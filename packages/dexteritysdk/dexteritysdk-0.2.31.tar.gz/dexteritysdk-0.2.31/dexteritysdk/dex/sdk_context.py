import threading
from io import BytesIO

import base58

from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple, Union

from borsh_construct import CStruct, U64, U32, U8
from solana.rpc import commitment, types
from solana.rpc.commitment import Confirmed
from solana.rpc.websocket_api import connect as solana_ws_connect
from solders.address_lookup_table_account import AddressLookupTableAccount
from solders.rpc.responses import AccountNotification, SubscriptionResult, SubscriptionError
from spl.token import instructions as spl_token_instructions

from dexteritysdk.codegen.instruments.types import DerivativeMetadata
from dexteritysdk.codegen.risk_engine.types import MarkPricesArray, UpdateMarkPricesParams
from dexteritysdk.pyserum.structs.event_queue import FillEvent, OutEvent
from dexteritysdk.pyserum.layouts.event_queue import Side
from dexteritysdk.pyserum.event_queue import EventQueue
from dexteritysdk.pyserum.orderbook import OrderBook

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from dexteritysdk.program_ids import SYSTEM_PROGRAM_ID as SYS_PROGRAM_ID
from solders.instruction import AccountMeta
from solana.transaction import Instruction
from solders import system_program

import dexteritysdk.codegen.dex.instructions as dixs
import dexteritysdk.codegen.dex.types as dtys
import dexteritysdk.codegen.risk_engine.instructions as rixs
from dexteritysdk import program_ids as pids, mints
from dexteritysdk.codegen.dex.accounts import Accounts as DexAccounts
from dexteritysdk.codegen.dex.constants import SENTINEL
from dexteritysdk.codegen.dex.types import MarketProductGroup, CancelOrderParams, ProductMetadata, account_tag
from dexteritysdk.codegen.risk_engine.accounts import Accounts as RiskEngineAccounts
from dexteritysdk.constant_fees import instructions as fee_ixs
from dexteritysdk.dex import addrs as daddrs
from dexteritysdk.dex.actions import DexOrderSummary
from dexteritysdk.utils import solana as solana_utils
from dexteritysdk.utils.aob import state as aaob_state
from dexteritysdk.codegen.instruments.accounts import Accounts as InstrumentAccounts
from dexteritysdk.utils.solana import Client, Context, AccountParser, explore, fetch_account_details, explore_many
from dexteritysdk.solmate.utils import to_account_meta


DEFAULT_MATCH_LIMIT = 16


class SDKEventType(Enum):
    SNAPSHOT = 1
    NEW = 2
    UPDATED = 3
    CLOSED = 4
    CANCELLED = 5
    FILLED = 6


@dataclass
class SDKFill:
    product: "SDKProduct"
    side: aaob_state.Side
    order_id: int
    qty: float
    price: float
    is_maker: bool
    taker_order_nonce: int


@dataclass
class SDKPosition:
    product: "SDKProduct"
    position: float
    pending_position: float
    last_cum_funding_snapshot: float
    last_social_loss_snapshot: float


@dataclass
class SDKOrder:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float
    client_order_id: int
    trader_risk_group: Pubkey

    @staticmethod
    def from_pyserum_orderbook(order_book: OrderBook, product: "SDKProduct", bids: bool) -> List["SDKOrder"]:
        return [
            SDKOrder(
                o.order_id,
                product,
                aaob_state.Side.BID if bids else aaob_state.Side.ASK,
                o.info.price,
                o.info.size,
                o.client_id,
                Pubkey.from_bytes(o.info.trader),
            ) for o in order_book.orders()
        ]


@dataclass
class SDKOrderSummary:
    order_id: int
    product: "SDKProduct"
    side: aaob_state.Side
    price: float
    qty: float
    filled_qty: float
    remaining_qty: float

    @staticmethod
    def from_dex_order_summary(sdk: "SDKContext", order_summary: DexOrderSummary, product: "SDKProduct",
                               side: aaob_state.Side, quantity: Union[dtys.Fractional, float],
                               price: Union[dtys.Fractional, float]) -> "SDKOrderSummary":
        if isinstance(quantity, dtys.Fractional):
            quantity = quantity.value
        if isinstance(price, dtys.Fractional):
            price = price.value
        order_id = None if order_summary.posted_order_id == order_summary.posted_order_id.NONE \
            else order_summary.posted_order_id.field
        if order_id:
            price = OrderBook.get_price_from_key(order_id, product.metadata.tick_size, product.metadata.price_offset)
        remaining_qty = order_summary.total_base_qty_posted / (10 ** sdk.decimals)
        filled_qty = quantity - remaining_qty
        return SDKOrderSummary(
            order_id=order_id,
            product=product,
            side=side,
            price=price,
            qty=quantity,
            filled_qty=filled_qty,
            remaining_qty=remaining_qty
        )


@dataclass
class SDKProduct:
    key: Pubkey
    index: int
    name: str  # max 16 bytes
    orderbook: Pubkey
    bids: Pubkey
    asks: Pubkey
    market_signer: Pubkey
    event_queue: Pubkey
    metadata: ProductMetadata  # last time prod was fetched
    price_oracle: Pubkey
    is_combo: bool
    _orderbook_data: "SDKOrderBook" = None

    def __hash__(self):
        return self.key.__hash__()

    def get_orderbook(self, sdk: "SDKContext", refresh: bool = False) -> "SDKOrderBook":
        if refresh or self._orderbook_data is None:
            self._orderbook_data = SDKOrderBook.from_product(sdk, self)
        return self._orderbook_data

    def crank_raw(self, sdk: "SDKContext", trader_and_risk_accounts: List[Pubkey], reward_target: Pubkey):
        trader_and_risk_accounts.sort()
        trader_and_risk_accounts = _dedup(trader_and_risk_accounts)
        ix = dixs.consume_orderbook_events(
            aaob_program=sdk.aaob_program,
            market_product_group=sdk.market_product_group,
            product=self.key,
            market_signer=self.market_signer,
            orderbook=self.orderbook,
            event_queue=self.event_queue,
            reward_target=reward_target,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            fee_output_register=sdk.fee_output_register,
            risk_and_fee_signer=daddrs.get_risk_signer(sdk.market_product_group),
            params=dtys.ConsumeOrderbookEventsParams(
                20
            ),
            remaining_accounts=[AccountMeta(pk, False, False) for pk in trader_and_risk_accounts]
        )
        solana_utils.send_instructions(ix)


def _dedup(xs):
    if len(xs) < 2:
        return xs
    i = 0
    for acct in xs[1:]:
        if xs[i] != acct:
            i += 1
            xs[i] = acct
    return xs[:i + 1]


@dataclass
class SDKOrderBook:
    product: SDKProduct
    bids: List[SDKOrder]
    asks: List[SDKOrder]
    slot: int

    @staticmethod
    def from_product(sdk: "SDKContext", product: "SDKProduct") -> "SDKOrderBook":
        ob_data = explore_many([product.bids, product.asks])
        bids_data = ob_data.data[0]
        asks_data = ob_data.data[1]

        return SDKOrderBook(
            product=product,
            bids=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(bids_data, product.metadata.base_decimals,
                                                product.metadata.price_offset, product.metadata.tick_size),
                product=product,
                bids=True,
            ),
            asks=SDKOrder.from_pyserum_orderbook(
                order_book=OrderBook.from_bytes(asks_data, product.metadata.base_decimals,
                                                product.metadata.price_offset, product.metadata.tick_size),
                product=product,
                bids=False,
            ),
            slot=ob_data.slot,
        )

    def find_order(self, order_id: int) -> SDKOrder:
        bid_match = next((o for o in self.bids if o.order_id == order_id), None)
        return bid_match if bid_match is not None else next((o for o in self.asks if o.order_id == order_id), None)


@dataclass
class _PendingNewOrder:
    product: Union[SDKProduct, Pubkey]
    side: aaob_state.Side
    size: Union[dtys.Fractional, float]
    price: Union[dtys.Fractional, float]
    self_trade_behavior: aaob_state.SelfTradeBehavior
    order_type: dtys.OrderType
    match_limit: int


@dataclass
class SDKTrader:
    keypair: Keypair
    account: Pubkey
    wallet: Pubkey
    trader_fee_state_acct: Pubkey
    trader_risk_state_acct: Pubkey  # separate pk vs kp to allow **vars(trader) in ixs
    whitelist_token_wallet: Pubkey
    staker_state: Pubkey

    _batches_lock: threading.Lock
    _batch_id: int
    _pending_batches: dict
    _seen_fills: set

    async def _monitor_accounts(
            self,
            sdk: "SDKContext",
            url: str,
            positions_callback: Callable[[List[SDKPosition], SDKEventType], Any],
            orders_callback: Callable[[List[SDKOrder], SDKEventType], Any],
            fills_callback: Callable[[SDKFill, SDKEventType], Any]
    ):
        def is_event_queue(acc: Pubkey) -> bool:
            return acc != self.account

        async for ws in solana_ws_connect(url):
            try:
                prev_trg = None
                trg, trg_slot = self.get_trader_risk_group()

                positions = None
                if positions_callback:
                    positions = list(self.open_positions(sdk, trg=trg))
                    positions_callback(positions, SDKEventType.SNAPSHOT)

                open_order_ids = defaultdict(set)
                if orders_callback:
                    open_orders = list(self.open_orders(sdk, trg=trg))
                    orders_callback(open_orders, SDKEventType.SNAPSHOT)
                    for o in open_orders:
                        open_order_ids[o.product].add(o.order_id)

                sub_to_pubkey = dict()
                event_queue_to_product = {product.event_queue: product for product in sdk.products}

                accounts = [product.event_queue for product in sdk.products]
                accounts.append(self.account)

                for account in accounts:
                    await ws.account_subscribe(account, commitment=commitment.Confirmed, encoding="base64")

                handled_orders = set()
                pending_products = set()

                def handle_cancelled_orders(product):
                    prev_open_order_ids = open_order_ids[product]

                    new_open_order_ids = set(
                        [order for _, order in self.open_order_ids(sdk, products=[product], trg=trg)]
                    )

                    open_order_ids[product] = new_open_order_ids

                    removed_order_ids = prev_open_order_ids.difference(new_open_order_ids)
                    for removed_order_id in removed_order_ids:
                        if removed_order_id in handled_orders:
                            handled_orders.remove(removed_order_id)
                            continue

                        removed_order_price = OrderBook.get_price_from_key(
                            removed_order_id,
                            product.metadata.tick_size,
                            product.metadata.price_offset
                        )
                        removed_order_side = aaob_state.Side.BID if OrderBook.key_is_bid(removed_order_id) \
                            else aaob_state.Side.ASK
                        removed_order_size = 0

                        removed_order_clordid = 0
                        if prev_trg is not None:
                            order_idx = prev_trg.open_orders.products[product.index].head_index
                            while order_idx != SENTINEL:
                                curr_order = prev_trg.open_orders.orders[order_idx]
                                if curr_order.id == removed_order_id:
                                    removed_order_size = curr_order.qty
                                    removed_order_clordid = curr_order.client_id
                                    break
                                order_idx = curr_order.next

                        orders_callback(
                            [SDKOrder(
                                removed_order_id,
                                product,
                                removed_order_side,
                                removed_order_price,
                                removed_order_size / (10 ** product.metadata.base_decimals),
                                removed_order_clordid,
                                self.account,
                            )],
                            SDKEventType.CANCELLED
                        )

                async for msgs in ws:
                    for msg in msgs:
                        if isinstance(msg, SubscriptionResult):
                            sub_to_pubkey[msg.result] = accounts[msg.id - 1]
                        elif isinstance(msg, SubscriptionError):
                            raise ValueError(f"Failed to subscribe [account={accounts[msg.id - 1]}, exc={msg}]")
                        elif isinstance(msg, AccountNotification):
                            notification_account = sub_to_pubkey[msg.subscription]
                            data = msg.result.value.data
                            slot = msg.result.context.slot
                            if is_event_queue(notification_account):
                                if fills_callback or orders_callback:
                                    product = event_queue_to_product[notification_account]
                                    event_queue = EventQueue.from_bytes(data)
                                    for e in event_queue:
                                        if isinstance(e, FillEvent) and fills_callback:
                                            order_nonce = e.taker_callback.order_nonce
                                            #print(f"saw order_nonce {order_nonce}")
                                            key = (order_nonce, e.maker_order_id)
                                            if key not in self._seen_fills:
                                                # print(f"got a heretounseen order_nonce {order_nonce}")
                                                self._seen_fills.add(key)
                                                # if we were the maker
                                                if e.maker_callback.account == self.account:
                                                    # convert taker to maker side
                                                    maker_side = aaob_state.Side.BID \
                                                        if e.taker_side == Side.ASK else aaob_state.Side.ASK
                                                    fill_size = e.base_size / (10 ** product.metadata.base_decimals)
                                                    quote_size = e.quote_size / (10 ** product.metadata.base_decimals)
                                                    fill_price = quote_size / fill_size if fill_size != 0.0 else float('NaN')
                                                    fills_callback(
                                                        SDKFill(
                                                            product,
                                                            maker_side,
                                                            e.maker_order_id,
                                                            fill_size,
                                                            fill_price,
                                                            True, # is_maker
                                                            order_nonce
                                                        ),
                                                        SDKEventType.NEW
                                                    )
                                                # else if we were the taker
                                                elif e.taker_callback.account == self.account:
                                                    taker_side = aaob_state.Side.ASK \
                                                        if e.taker_side == Side.ASK else aaob_state.Side.BID
                                                    fill_size = e.base_size / (10 ** product.metadata.base_decimals)
                                                    quote_size = e.quote_size / (10 ** product.metadata.base_decimals)
                                                    fill_price = quote_size / fill_size if fill_size != 0.0 else float('NaN')
                                                    fills_callback(
                                                        SDKFill(
                                                            product,
                                                            taker_side,
                                                            None,
                                                            fill_size,
                                                            fill_price,
                                                            False, # is_maker
                                                            order_nonce
                                                        ),
                                                        SDKEventType.NEW
                                                    )
                                        elif isinstance(e, OutEvent) and orders_callback:
                                            if e.callback.account == self.account:
                                                handled_orders.add(e.order_id)
                                                event_type = SDKEventType.FILLED if e.base_size == 0 \
                                                    else SDKEventType.CANCELLED
                                                side = aaob_state.Side.BID if OrderBook.key_is_bid(e.order_id) \
                                                    else aaob_state.Side.ASK
                                                price = OrderBook.get_price_from_key(
                                                    e.order_id,
                                                    product.metadata.tick_size,
                                                    product.metadata.price_offset
                                                )
                                                orders_callback(
                                                    [SDKOrder(
                                                        e.order_id,
                                                        product,
                                                        side,
                                                        price,
                                                        e.base_size / (10 ** product.metadata.base_decimals),
                                                        e.callback.client_order_id,
                                                        self.account,
                                                    )],
                                                    event_type
                                                )

                                    # try to infer what happened to the rest of our open orders
                                    if orders_callback:
                                        if slot != trg_slot:
                                            pending_products.add(product)
                                            continue

                                        handle_cancelled_orders(product)
                            else:
                                prev_trg = trg
                                trg = DexAccounts.from_bytes(data).field
                                trg_slot = slot

                                for p in pending_products:
                                    handle_cancelled_orders(p)

                                pending_products = set()

                                if positions_callback:
                                    new_positions = list(self.open_positions(sdk, trg))
                                    for position in positions:
                                        new_position = next(
                                            (p for p in new_positions if p.product == position.product),
                                            None
                                        )
                                        # if position was closed
                                        if not new_position:
                                            positions_callback([SDKPosition(position.product, 0, 0, 0, 0)],
                                                               SDKEventType.CLOSED)
                                        # if existing position has changed
                                        elif position != new_position:
                                            positions_callback([new_position], SDKEventType.UPDATED)

                                    for new_position in new_positions:
                                        old_position = next(
                                            (p for p in positions if p.product == new_position.product),
                                            None
                                        )
                                        # if new position
                                        if not old_position:
                                            positions_callback([new_position], SDKEventType.NEW)

                                    positions = new_positions

                        else:
                            print(f"Unknown msg: {msg}")
            except Exception as e:
                print(f"Monitoring Exception: {str(e)}")
                continue

    async def subscribe(
            self,
            sdk: "SDKContext",
            ws_url: str,
            positions_callback: Callable[[List[SDKPosition], SDKEventType], Any] = None,
            orders_callback: Callable[[List[SDKOrder], SDKEventType], Any] = None,
            fills_callback: Callable[[SDKFill, SDKEventType], Any] = None,
    ):
        await self._monitor_accounts(sdk, ws_url, positions_callback, orders_callback, fills_callback)

    @staticmethod
    def connect(
            sdk: "SDKContext",
            account: Pubkey,
            keypair: Keypair,
    ) -> "SDKTrader":
        wallet = spl_token_instructions.get_associated_token_address(keypair.pubkey(), sdk.vault_mint)

        trg: dtys.TraderRiskGroup = explore(account).data_obj
        assert trg.market_product_group == sdk.market_product_group
        assert trg.owner == keypair.pubkey()

        whitelist_token_wallet = spl_token_instructions.get_associated_token_address(
            keypair.pubkey(),
            mints.WHITELIST_TOKEN_MINT
        )

        staker_state_key, _ = Pubkey.find_program_address(
            seeds=[
                bytes(keypair.pubkey()),
                bytes(sdk.stake_pool)
            ],
            program_id=sdk.staking_program
        )

        return SDKTrader(
            keypair, account, wallet, trg.fee_state_account, trg.risk_state_account, whitelist_token_wallet,
            staker_state=staker_state_key, _batches_lock=threading.Lock(), _batch_id=0, _pending_batches={}, _seen_fills=set())

    def get_trader_risk_group(self) -> Tuple[dtys.TraderRiskGroup, int]:
        account_details = fetch_account_details(self.account)
        return account_details.data_obj, account_details.slot

    def deposit(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * (10 ** sdk.decimals)), sdk.decimals)
        ix = dixs.deposit_funds(
            user=self.keypair.pubkey(),
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            capital_limits=sdk.capital_limits,
            params=dtys.DepositFundsParams(
                quantity=qty,
            ),
            program_id=sdk.dex_program,
        )
        return sdk.send_instructions(ix)

    def withdraw(self, sdk: "SDKContext", qty: Union[float, dtys.Fractional]):
        if not isinstance(qty, dtys.Fractional):
            qty = dtys.Fractional(int(qty * 10**sdk.decimals), sdk.decimals)

        remaining_accounts = [
            to_account_meta(ra, is_signer=False, is_writable=True) for ra in sdk.additional_risk_accts
        ]

        ix = dixs.withdraw_funds(
            user=self.keypair.pubkey(),
            user_token_account=self.wallet,
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            market_product_group_vault=sdk.market_product_group_vault,
            risk_output_register=sdk.risk_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_signer=sdk.risk_signer,
            capital_limits=sdk.capital_limits,
            trader_risk_state_acct=self.trader_risk_state_acct,
            params=dtys.WithdrawFundsParams(
                quantity=qty,
            ),
            program_id=sdk.dex_program,
            remaining_accounts=remaining_accounts,
        )
        return sdk.send_instructions(ix)

    def init_batch(self):
        self._batches_lock.acquire()
        batch_id = self._batch_id
        self._batch_id += 1
        self._batches_lock.release()
        self._pending_batches[batch_id] = []
        return batch_id

    def commit_batch(self, sdk: "SDKContext", batch_id: int) -> List[SDKOrderSummary]:
        if batch_id not in self._pending_batches:
            raise ValueError("Invalid batch_id")

        pending_actions = self._pending_batches.pop(batch_id)
        assert(pending_actions and len(pending_actions) > 0)

        ixs = []
        pending_places = []
        for a in pending_actions:
            if isinstance(a, _PendingNewOrder):
                pending_places.append(a)
                ixs.append(self._place_order_ix(sdk, a.product, a.side, a.size, a.price, a.self_trade_behavior,
                                                a.order_type, sdk.additional_risk_accts, match_limit=a.match_limit))
            else:
                ixs.append(a)

        ixs.insert(0, self._request_compute_ix(sdk))

        trans_details = sdk.send_instructions(*ixs, raise_on_error=False)
        if trans_details.error:
            raise ValueError(trans_details.error_from_log if trans_details.error_from_log is not None else trans_details.error)
        else:
            return [
                SDKOrderSummary.from_dex_order_summary(
                    sdk,
                    DexOrderSummary.from_bytes(raw_summary),
                    pending_places[idx].product,
                    pending_places[idx].side,
                    pending_places[idx].size,
                    pending_places[idx].price
                ) for idx, raw_summary in enumerate(trans_details.emitted_dex_order_summaries())
            ]

    def _request_compute_ix(self, sdk: "SDKContext", units: int = 1400000):
        request_units = CStruct(
            "units" / U32,
        )

        buffer = BytesIO()
        # this is the enum value for SetComputeUnitLimit
        buffer.write(U8.build(2))
        buffer.write(request_units.build({"units": units}))

        return Instruction(
            accounts=[],
            program_id=Pubkey.from_string("ComputeBudget111111111111111111111111111111"),
            data=buffer.getvalue()
        )

    def _set_compute_unit_price_ix(self, sdk: "SDKContext", microLamports: int = 5000):
        compute_unit_price = CStruct(
            "microLamports" / U64,
        )

        buffer = BytesIO()
        # this is the enum value for SetComputeUnitPrice
        buffer.write(U8.build(3))
        buffer.write(compute_unit_price.build({"microLamports": microLamports}))

        return Instruction(
            accounts=[],
            program_id=Pubkey.from_string("ComputeBudget111111111111111111111111111111"),
            data=buffer.getvalue()
        )

    def place_order(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, Pubkey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            batch_id: int = None,
            client_order_id: int = 0,
            match_limit: int = DEFAULT_MATCH_LIMIT,
    ) -> SDKOrderSummary:
        ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                  sdk.additional_risk_accts, client_order_id=client_order_id, match_limit=match_limit)
        if batch_id is not None:
            self._pending_batches[batch_id].append(_PendingNewOrder(product, side, size, price, self_trade_behavior, order_type, match_limit))
        else:
            request_compute_ix = self._request_compute_ix(sdk, 800000)
            trans_details = sdk.send_instructions(request_compute_ix, ix, raise_on_error=False)
            if trans_details.error:
                raise ValueError(trans_details.error_from_log if trans_details.error_from_log is not None else trans_details.error)
            else:
                raw_summary = trans_details.emitted_logs["new-order:order-summary"]
                return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                              product, side, size, price)

    def _place_order_ix(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, Pubkey],
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            risk_accounts: Optional[List[Pubkey]] = None,
            referrer_trg: Optional[Pubkey] = None,
            referrer_fee_bps: dtys.Fractional = dtys.Fractional(0, 0),
            client_order_id: int = 0,
            match_limit: int = DEFAULT_MATCH_LIMIT,
    ):
        remaining_accounts = [to_account_meta(ra, is_signer=False, is_writable=True) for ra in risk_accounts]
        remaining_accounts.append(to_account_meta(sdk.stake_pool, is_signer=False, is_writable=True))
        remaining_accounts.append(to_account_meta(self.staker_state, is_signer=False, is_writable=True))

        if referrer_trg is None:
            referrer_trg = self.account

        ix = dixs.new_order(
            program_id=sdk.dex_program,
            user=self.keypair.pubkey(),
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            fee_model_program=sdk.fee_model_program,
            fee_model_configuration_acct=sdk.fee_model_configuration_acct,
            trader_fee_state_acct=self.trader_fee_state_acct,
            fee_output_register=sdk.fee_output_register,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_and_fee_signer=sdk.risk_signer,
            referrer_trg=referrer_trg,
            params=dtys.NewOrderParams(
                side=side,
                max_base_qty=dtys.Fractional.into(size, product.metadata.base_decimals),
                order_type=order_type,
                self_trade_behavior=self_trade_behavior,
                match_limit=match_limit,
                limit_price=dtys.Fractional.into(price, 8).simplify(),
                referrer_fee_bps=referrer_fee_bps,
                client_order_id=client_order_id,
            ),
            remaining_accounts=remaining_accounts,
        )

        return ix

    def cancel(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            batch_id: int = None,
            client_order_id: int = 0,
    ):
        self.cancel_underwater(sdk, product, order_id, self.account, batch_id=batch_id, client_order_id=client_order_id)

    def cancel_underwater(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: Pubkey,
            batch_id: int = None,
            no_err: bool = False,
            client_order_id: int = 0,
    ):
        if batch_id is not None:
            self._pending_batches[batch_id].append(self._cancel_ix(sdk, product, order_id, under_water_trg, no_err, client_order_id))
        else:
            update_variance_cache_ix = self._update_variance_cache_ix(sdk)
            ix = self._cancel_ix(sdk, product, order_id, under_water_trg, no_err, client_order_id)
            trans_details = sdk.send_instructions(ix, update_variance_cache_ix, raise_on_error=False)
            if trans_details.error:
                raise ValueError(f"{order_id}: {trans_details.error_from_log if trans_details.error_from_log is not None else trans_details.error}")

    def _update_variance_cache_ix(
            self,
            sdk: "SDKContext"
    ):
        remaining_accounts = [
            to_account_meta(ra, is_signer=False, is_writable=True) for ra in sdk.additional_risk_accts
        ]

        return dixs.update_variance_cache(
            payer=self.keypair.pubkey(),
            trader_risk_group=self.account,
            market_product_group=sdk.market_product_group,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_and_fee_signer=sdk.risk_signer,
            remaining_accounts=remaining_accounts
        )

    def update_mark_prices(
            self,
            sdk: "SDKContext"
    ):
        for products in self._chunks(sdk.products, 3):
            sdk.send_instructions(self._update_mark_prices_ix(sdk, products))

    def _update_mark_prices_ix(
            self,
            sdk: "SDKContext",
            products: List["SDKProduct"],
    ):
        remaining_accounts = []

        num_products = 0

        for product in products:
            if product.is_combo:
                continue
            for acc in [product.key, product.price_oracle, product.orderbook, product.bids, product.asks]:
                remaining_accounts.append(to_account_meta(acc, is_signer=False, is_writable=True))
            num_products = num_products + 1

        ix = rixs.update_mark_prices(
            payer=self.keypair.pubkey(),
            mark_prices=sdk.additional_risk_accts[2],
            market_product_group=sdk.market_product_group,
            remaining_accounts=remaining_accounts,
            params=UpdateMarkPricesParams(num_products=num_products),
        )

        return ix

    def _cancel_ix(
            self,
            sdk: "SDKContext",
            product: SDKProduct,
            order_id: int,
            under_water_trg: Pubkey,
            no_err: bool,
            client_order_id: int,
    ):
        return dixs.cancel_order(
            user=self.keypair.pubkey(),
            trader_risk_group=under_water_trg,
            market_product_group=sdk.market_product_group,
            product=product.key,
            aaob_program=sdk.aaob_program,
            orderbook=product.orderbook,
            market_signer=product.market_signer,
            event_queue=product.event_queue,
            bids=product.bids,
            asks=product.asks,
            risk_engine_program=sdk.risk_engine_program,
            risk_model_configuration_acct=sdk.risk_model_configuration_acct,
            risk_output_register=sdk.risk_output_register,
            trader_risk_state_acct=self.trader_risk_state_acct,
            risk_signer=sdk.risk_signer,
            params=CancelOrderParams(order_id=order_id, no_err=[1] if no_err else [0], client_order_id=client_order_id),
            remaining_accounts=None,
            program_id=sdk.dex_program,
        )

        # workaround to correctly serialize no_err
#        ix_data = bytearray(ix.data)
#        if len(ix_data) < 25:
#            ix_data.append(0)
#        if no_err:
#            ix_data = ix_data[:-1] + b'\x01'


    def replace(
            self,
            sdk: "SDKContext",
            product: Union[SDKProduct, Pubkey],
            order_id: int,
            side: aaob_state.Side,
            size: Union[dtys.Fractional, float],
            price: Union[dtys.Fractional, float],
            self_trade_behavior: aaob_state.SelfTradeBehavior = aaob_state.SelfTradeBehavior.CANCEL_PROVIDE,
            order_type: dtys.OrderType = dtys.OrderType.LIMIT,
            batch_id: int = None,
            cancel_no_err: bool = True,
            client_order_id: int = 0,
            match_limit: int = DEFAULT_MATCH_LIMIT,
    ) -> DexOrderSummary:
        cancel_ix = self._cancel_ix(sdk, product, order_id, self.account, no_err=cancel_no_err, client_order_id=client_order_id)
        place_ix = self._place_order_ix(sdk, product, side, size, price, self_trade_behavior, order_type,
                                        sdk.additional_risk_accts, client_order_id=client_order_id, match_limit=match_limit)

        if batch_id is not None:
            self._pending_batches[batch_id].append(cancel_ix)
            self._pending_batches[batch_id].append(_PendingNewOrder(product, side, size, price, self_trade_behavior, order_type, match_limit))
        else:
            request_compute_ix = self._request_compute_ix(sdk, 800000)
            trans_details = sdk.send_instructions(request_compute_ix, cancel_ix, place_ix, raise_on_error=False)
            if trans_details.error:
                raise Exception(trans_details.error_from_log if trans_details.error_from_log is not None else trans_details.error)
            else:
                raw_summary = trans_details.emitted_logs["new-order:order-summary"]
                return SDKOrderSummary.from_dex_order_summary(sdk, DexOrderSummary.from_bytes(raw_summary),
                                                              product, side, size, price)

    def open_positions(
            self,
            sdk: "SDKContext",
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKPosition]:
        if not trg:
            trg, _ = self.get_trader_risk_group()
        for position in trg.trader_positions:
            if position.tag == account_tag.AccountTag.UNINITIALIZED or \
                    (position.position.value == 0 and position.pending_position.value == 0):
                continue
            yield SDKPosition(
                next(product for product in sdk.products if product.key == position.product_key),
                position.position.value,
                position.pending_position.value,
                position.last_cum_funding_snapshot.value,
                position.last_social_loss_snapshot.value
            )

    def open_orders(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKOrder]:
        if products is None or len(products) == 0:
            products = sdk.products

        if not trg:
            trg, slot = self.get_trader_risk_group()
            # print(f"fetched trg at slot {slot}")
        for p in products:
            ptr = trg.open_orders.products[p.index].head_index
            order = trg.open_orders.orders[ptr]
            assert order.prev == SENTINEL
            while ptr != SENTINEL:
                order = trg.open_orders.orders[ptr]
                assert order.id != 0
                yield SDKOrder(
                    order.id,
                    p,
                    aaob_state.Side.BID if OrderBook.key_is_bid(order.id) else aaob_state.Side.ASK,
                    OrderBook.get_price_from_key(order.id, p.metadata.tick_size, p.metadata.price_offset),
                    order.qty / (10 ** p.metadata.base_decimals),
                    order.client_id,
                    self.account,
                )
                ptr = order.next

    def open_order_ids(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            trg: dtys.TraderRiskGroup = None
    ) -> Iterable[SDKProduct, int]:
        if products is None or len(products) == 0:
            products = sdk.products

        if not trg:
            trg, _ = self.get_trader_risk_group()
        for p in products:
            ptr = trg.open_orders.products[p.index].head_index
            order = trg.open_orders.orders[ptr]
            assert order.prev == SENTINEL
            while ptr != SENTINEL:
                order = trg.open_orders.orders[ptr]
                assert order.id != 0
                yield p, order.id
                ptr = order.next

    def _chunks(self, lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def cancel_all_orders(
            self,
            sdk: "SDKContext",
            products: List[SDKProduct] = None,
            no_err: bool = True,
            batch_size: int = 8
    ):
        if products is None or len(products) == 0:
            products = sdk.products

        update_variance_cache_ix = self._update_variance_cache_ix(sdk)

        for p in products:
            open_orders = self.open_order_ids(sdk, [p])
            ixs = [self._cancel_ix(sdk, p, o, self.account, no_err, 0) for p, o in open_orders]

            # batch cancels in tx's of batch_size
            for chunk in self._chunks(ixs, batch_size):
                sdk.send_instructions(*chunk, update_variance_cache_ix)


@dataclass
class SDKContext:
    product_group_name: str  # max 16 chars
    trader_risk_state_account_len: int
    decimals: int
    # cached products, reload if necessary
    products: List[SDKProduct]
    # program_ids
    dex_program: Pubkey
    aaob_program: Pubkey
    risk_engine_program: Pubkey
    instruments_program: Pubkey
    # dummy_oracle_program_id: Pubkey
    fee_model_program: Pubkey
    staking_program: Pubkey
    # accts
    market_product_group: Pubkey
    capital_limits: Pubkey
    payer: Keypair
    market_product_group_vault: Pubkey
    vault_mint: Pubkey
    fee_model_configuration_acct: Pubkey
    risk_model_configuration_acct: Pubkey
    risk_signer: Pubkey
    fee_signer: Pubkey
    risk_output_register: Pubkey
    fee_output_register: Pubkey
    fee_collector: Pubkey
    stake_pool: Pubkey
    additional_risk_accts: List[Pubkey]
    address_lookup_table_account: Optional[AddressLookupTableAccount]

    @staticmethod
    def connect(client: Client,
                payer: Keypair,
                market_product_group_key: Pubkey,
                trader_risk_state_account_len: int = 0,
                dex_program_id: Pubkey = pids.DEX_PROGRAM_ID,
                aaob_program_id: Pubkey = pids.AOB_PROGRAM_ID,
                risk_engine_program_id: Pubkey = pids.RISK_ENGINE_PROGRAM_ID,
                instruments_program_id: Pubkey = pids.INSTRUMENTS_PROGRAM_ID,
                staking_program_id: Pubkey = pids.STAKING_PROGRAM_ID,
                stake_pool: Pubkey = Pubkey.from_string("9zdpqAgENj4734TQvqjczMg2ekvvuGsxwJC6f7F1QWp4"),
                raise_on_error: bool = False,
                **kwargs):
        parser = AccountParser()
        parser.register_parser_from_account_enum(pids.DEX_PROGRAM_ID, DexAccounts)
        parser.register_parser_from_account_enum(pids.RISK_ENGINE_PROGRAM_ID, RiskEngineAccounts)
        parser.register_parser(pids.AOB_PROGRAM_ID, aaob_state.account_parser)
        parser.register_parser_from_account_enum(pids.INSTRUMENTS_PROGRAM_ID, InstrumentAccounts)
        Context.init_globals(
            fee_payer=payer,
            client=client,
            signers=[(payer, "payer")],
            parser=parser,
            raise_on_error=raise_on_error,
        )

        mpg: MarketProductGroup = solana_utils.explore(market_product_group_key).data_obj

        address_lookup_table_account = None
        try:
            address_lookup_table_account = solana_utils.get_address_lookup_table_account(mpg.address_lookup_table)
        except:
            pass

        capital_limits_key, _ = Pubkey.find_program_address(
            [b"capital_limits_state", bytes(market_product_group_key)],
            dex_program_id
        )

        s_account, _ = Pubkey.find_program_address(
            [b"s", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        r_account, _ = Pubkey.find_program_address(
            [b"r", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        mark_prices_account, _ = Pubkey.find_program_address(
            [b"mark_prices", bytes(market_product_group_key)],
            risk_engine_program_id
        )

        sdk_context = SDKContext(
            product_group_name=bytes(mpg.name).decode("utf-8").strip(),
            trader_risk_state_account_len=trader_risk_state_account_len,
            decimals=mpg.decimals,
            # cached products reload if necessary
            products=[],
            # program_ids
            dex_program=dex_program_id,
            aaob_program=aaob_program_id,
            risk_engine_program=risk_engine_program_id,
            instruments_program=instruments_program_id,
            # dummy_oracle_program_id=None,
            fee_model_program=mpg.fee_model_program_id,
            staking_program=staking_program_id,
            # accts
            market_product_group=market_product_group_key,
            capital_limits=capital_limits_key,
            payer=payer,
            market_product_group_vault=daddrs.get_market_product_group_vault(market_product_group_key),
            vault_mint=mpg.vault_mint,
            fee_model_configuration_acct=mpg.fee_model_configuration_acct,
            risk_model_configuration_acct=mpg.risk_model_configuration_acct,
            risk_signer=daddrs.get_risk_signer(market_product_group_key),
            fee_signer=daddrs.get_risk_signer(market_product_group_key),
            risk_output_register=mpg.risk_output_register,
            fee_output_register=mpg.fee_output_register,
            fee_collector=mpg.fee_collector,
            stake_pool=stake_pool,
            additional_risk_accts=[s_account, r_account, mark_prices_account],
            address_lookup_table_account=address_lookup_table_account,
        )
        sdk_context.load_products()
        return sdk_context

    def list_trader_risk_groups(self) -> List[Pubkey]:
        account_discriminator_filter = types.MemcmpOpts(
            offset=0,
            bytes=str(base58.b58encode(
                int(DexAccounts.TRADER_RISK_GROUP).to_bytes(8, "little")
            ), 'utf-8')
        )
        mpg_filter = types.MemcmpOpts(
            offset=16,
            bytes=str(base58.b58encode(bytes(self.market_product_group)), 'utf-8')
        )
        trader_filter = types.MemcmpOpts(
            offset=48,
            bytes=str(base58.b58encode(bytes(self.payer.pubkey())), 'utf-8')
        )
        response = Context.get_global_client().get_program_accounts(
            pubkey=self.dex_program,
            commitment=Confirmed,
            encoding="base64",
            data_slice=types.DataSliceOpts(offset=0, length=0),  # we don't need any data
            filters=[account_discriminator_filter, mpg_filter, trader_filter]
        )
        trgs = []
        for account in response.value:
            trgs.append(account.pubkey)
        return trgs

    def load_mpg(self) -> MarketProductGroup:
        return fetch_account_details(self.market_product_group).data_obj

    def load_mark_prices(self) -> MarkPricesArray:
        return fetch_account_details(self.additional_risk_accts[2]).data_obj

    def get_mark_price(self, product_key: Pubkey) -> dtys.Fractional:
        return self.extract_mark_price(self.load_mark_prices(), product_key)

    def extract_mark_price(self, mark_prices_array: MarkPricesArray, product_key: Pubkey) -> dtys.Fractional:
        for mp in mark_prices_array.array:
            if mp.product_key == product_key:
                return dtys.Fractional(mp.mark_price.value, 6)
        raise ValueError(f"extract_mark_price failed because no such product found on mark prices array: {product_key}")

    def get_oracle_minus_book_ewma(self, product_key: Pubkey) -> dtys.Fractional:
        return self.extract_oracle_minus_book_ewma(self.load_mark_prices(), product_key)

    def extract_oracle_minus_book_ewma(self, mark_prices_array: MarkPricesArray, product_key: Pubkey) -> dtys.Fractional:
        for mp in mark_prices_array.array:
            if mp.product_key == product_key:
                return dtys.Fractional(mp.oracle_minus_book_ewma.value, 6)
        raise ValueError(f"extract_oracle_minus_book_ewma failed because no such product found on mark prices array: {product_key}")

    def get_index_price(self, product_key: Pubkey) -> dtys.Fractional:
        return self.extract_index_price(self.load_mark_prices(), product_key)

    def extract_index_price(self, mark_prices_array: MarkPricesArray, product_key: Pubkey) -> dtys.Fractional:
        mark_price = self.extract_mark_price(mark_prices_array, product_key)
        ema = self.extract_oracle_minus_book_ewma(mark_prices_array, product_key)
        return mark_price + ema

    def load_products(self):
        mpg = self.load_mpg()
        products = []

        mark_prices: MarkPricesArray = fetch_account_details(self.additional_risk_accts[2]).data_obj

        for idx, prod in mpg.active_products():
            if mpg.is_expired(prod):
                continue
            metadata = prod.metadata()
            product_name = bytes(metadata.name).decode('utf-8').strip()
            try:
                orderbook: aaob_state.MarketState = fetch_account_details(metadata.orderbook).data_obj

                price_oracle = None
                if mark_prices.is_hardcoded_oracle:
                    price_oracle = mark_prices.hardcoded_oracle
                elif not mark_prices.is_hardcoded_oracle and prod.is_outright():
                    derivative_metadata: DerivativeMetadata = fetch_account_details(metadata.product_key).data_obj
                    price_oracle = derivative_metadata.price_oracle

                products.append(
                    SDKProduct(
                        metadata.product_key,
                        idx,
                        product_name,
                        orderbook=metadata.orderbook,
                        asks=orderbook.asks,
                        bids=orderbook.bids,
                        event_queue=orderbook.event_queue,
                        market_signer=daddrs.get_market_signer(metadata.product_key),
                        metadata=metadata,
                        price_oracle=price_oracle,
                        is_combo=prod.is_combo(),
                    )
                )
            except:
                print(f"WARNING: Ignoring invalid product {product_name}")
                continue

        self.products = products

    def send_instructions(self, *ixs: Instruction, **kwargs):
        return solana_utils.send_instructions(*ixs, **kwargs, address_lookup_table_accounts=[self.address_lookup_table_account] if self.address_lookup_table_account else None)

    def register_trader(self, keypair: Keypair):
        trader_risk_group = Keypair()
        trader_risk_state_acct = Keypair()
        _ident = str(keypair.pubkey())[:8]
        Context.add_signers(
            (trader_risk_state_acct, f"{_ident}'s {Context.trader_nonce}-th trader_risk_state_acct"),
            (trader_risk_group, f"{_ident}'s {Context.trader_nonce}-th trader_risk_group)"),
        )
        Context.trader_nonce += 1
        trader_fee_state_acct = daddrs.get_trader_fee_state_acct(
            trader_risk_group.pubkey(),
            self.market_product_group,
            self.fee_model_configuration_acct,
            self.fee_model_program
        )

        size = 13272
        allocate_trg = system_program.create_account(
            system_program.CreateAccountParams(
                from_pubkey=self.payer.pubkey(),
                to_pubkey=trader_risk_group.pubkey(),
                lamports=solana_utils.calc_rent(size),
                space=size,
                owner=self.dex_program,
            )
        )
        trg_init_ix = dixs.initialize_trader_risk_group(
            owner=keypair.pubkey(),
            trader_risk_group=trader_risk_group.pubkey(),
            trader_risk_state_acct=trader_risk_state_acct.pubkey(),
            trader_fee_state_acct=trader_fee_state_acct,
            market_product_group=self.market_product_group,
            risk_signer=self.risk_signer,
            risk_engine_program=self.risk_engine_program,
            fee_model_config_acct=self.fee_model_configuration_acct,
            fee_model_program=self.fee_model_program,
            program_id=self.dex_program,
            # **vars(self),
        )
        self.send_instructions(allocate_trg, trg_init_ix)
        return SDKTrader.connect(
            self,
            trader_risk_group.pubkey(),
            keypair,
        )
