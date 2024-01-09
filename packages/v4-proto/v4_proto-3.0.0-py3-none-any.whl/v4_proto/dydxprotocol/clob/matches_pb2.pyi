from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as _subaccount_pb2
from v4_proto.dydxprotocol.clob import order_pb2 as _order_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClobMatch(_message.Message):
    __slots__ = ("match_orders", "match_perpetual_liquidation", "match_perpetual_deleveraging")
    MATCH_ORDERS_FIELD_NUMBER: _ClassVar[int]
    MATCH_PERPETUAL_LIQUIDATION_FIELD_NUMBER: _ClassVar[int]
    MATCH_PERPETUAL_DELEVERAGING_FIELD_NUMBER: _ClassVar[int]
    match_orders: MatchOrders
    match_perpetual_liquidation: MatchPerpetualLiquidation
    match_perpetual_deleveraging: MatchPerpetualDeleveraging
    def __init__(self, match_orders: _Optional[_Union[MatchOrders, _Mapping]] = ..., match_perpetual_liquidation: _Optional[_Union[MatchPerpetualLiquidation, _Mapping]] = ..., match_perpetual_deleveraging: _Optional[_Union[MatchPerpetualDeleveraging, _Mapping]] = ...) -> None: ...

class MakerFill(_message.Message):
    __slots__ = ("fill_amount", "maker_order_id")
    FILL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    MAKER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    fill_amount: int
    maker_order_id: _order_pb2.OrderId
    def __init__(self, fill_amount: _Optional[int] = ..., maker_order_id: _Optional[_Union[_order_pb2.OrderId, _Mapping]] = ...) -> None: ...

class MatchOrders(_message.Message):
    __slots__ = ("taker_order_id", "fills")
    TAKER_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    FILLS_FIELD_NUMBER: _ClassVar[int]
    taker_order_id: _order_pb2.OrderId
    fills: _containers.RepeatedCompositeFieldContainer[MakerFill]
    def __init__(self, taker_order_id: _Optional[_Union[_order_pb2.OrderId, _Mapping]] = ..., fills: _Optional[_Iterable[_Union[MakerFill, _Mapping]]] = ...) -> None: ...

class MatchPerpetualLiquidation(_message.Message):
    __slots__ = ("liquidated", "clob_pair_id", "perpetual_id", "total_size", "is_buy", "fills")
    LIQUIDATED_FIELD_NUMBER: _ClassVar[int]
    CLOB_PAIR_ID_FIELD_NUMBER: _ClassVar[int]
    PERPETUAL_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SIZE_FIELD_NUMBER: _ClassVar[int]
    IS_BUY_FIELD_NUMBER: _ClassVar[int]
    FILLS_FIELD_NUMBER: _ClassVar[int]
    liquidated: _subaccount_pb2.SubaccountId
    clob_pair_id: int
    perpetual_id: int
    total_size: int
    is_buy: bool
    fills: _containers.RepeatedCompositeFieldContainer[MakerFill]
    def __init__(self, liquidated: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., clob_pair_id: _Optional[int] = ..., perpetual_id: _Optional[int] = ..., total_size: _Optional[int] = ..., is_buy: bool = ..., fills: _Optional[_Iterable[_Union[MakerFill, _Mapping]]] = ...) -> None: ...

class MatchPerpetualDeleveraging(_message.Message):
    __slots__ = ("liquidated", "perpetual_id", "fills", "is_final_settlement")
    class Fill(_message.Message):
        __slots__ = ("offsetting_subaccount_id", "fill_amount")
        OFFSETTING_SUBACCOUNT_ID_FIELD_NUMBER: _ClassVar[int]
        FILL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
        offsetting_subaccount_id: _subaccount_pb2.SubaccountId
        fill_amount: int
        def __init__(self, offsetting_subaccount_id: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., fill_amount: _Optional[int] = ...) -> None: ...
    LIQUIDATED_FIELD_NUMBER: _ClassVar[int]
    PERPETUAL_ID_FIELD_NUMBER: _ClassVar[int]
    FILLS_FIELD_NUMBER: _ClassVar[int]
    IS_FINAL_SETTLEMENT_FIELD_NUMBER: _ClassVar[int]
    liquidated: _subaccount_pb2.SubaccountId
    perpetual_id: int
    fills: _containers.RepeatedCompositeFieldContainer[MatchPerpetualDeleveraging.Fill]
    is_final_settlement: bool
    def __init__(self, liquidated: _Optional[_Union[_subaccount_pb2.SubaccountId, _Mapping]] = ..., perpetual_id: _Optional[int] = ..., fills: _Optional[_Iterable[_Union[MatchPerpetualDeleveraging.Fill, _Mapping]]] = ..., is_final_settlement: bool = ...) -> None: ...
