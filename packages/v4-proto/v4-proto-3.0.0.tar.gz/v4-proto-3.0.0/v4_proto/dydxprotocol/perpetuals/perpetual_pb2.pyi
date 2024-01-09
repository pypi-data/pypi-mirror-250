from v4_proto.gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Perpetual(_message.Message):
    __slots__ = ("params", "funding_index")
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    FUNDING_INDEX_FIELD_NUMBER: _ClassVar[int]
    params: PerpetualParams
    funding_index: bytes
    def __init__(self, params: _Optional[_Union[PerpetualParams, _Mapping]] = ..., funding_index: _Optional[bytes] = ...) -> None: ...

class PerpetualParams(_message.Message):
    __slots__ = ("id", "ticker", "market_id", "atomic_resolution", "default_funding_ppm", "liquidity_tier")
    ID_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    MARKET_ID_FIELD_NUMBER: _ClassVar[int]
    ATOMIC_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FUNDING_PPM_FIELD_NUMBER: _ClassVar[int]
    LIQUIDITY_TIER_FIELD_NUMBER: _ClassVar[int]
    id: int
    ticker: str
    market_id: int
    atomic_resolution: int
    default_funding_ppm: int
    liquidity_tier: int
    def __init__(self, id: _Optional[int] = ..., ticker: _Optional[str] = ..., market_id: _Optional[int] = ..., atomic_resolution: _Optional[int] = ..., default_funding_ppm: _Optional[int] = ..., liquidity_tier: _Optional[int] = ...) -> None: ...

class MarketPremiums(_message.Message):
    __slots__ = ("perpetual_id", "premiums")
    PERPETUAL_ID_FIELD_NUMBER: _ClassVar[int]
    PREMIUMS_FIELD_NUMBER: _ClassVar[int]
    perpetual_id: int
    premiums: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, perpetual_id: _Optional[int] = ..., premiums: _Optional[_Iterable[int]] = ...) -> None: ...

class PremiumStore(_message.Message):
    __slots__ = ("all_market_premiums", "num_premiums")
    ALL_MARKET_PREMIUMS_FIELD_NUMBER: _ClassVar[int]
    NUM_PREMIUMS_FIELD_NUMBER: _ClassVar[int]
    all_market_premiums: _containers.RepeatedCompositeFieldContainer[MarketPremiums]
    num_premiums: int
    def __init__(self, all_market_premiums: _Optional[_Iterable[_Union[MarketPremiums, _Mapping]]] = ..., num_premiums: _Optional[int] = ...) -> None: ...

class LiquidityTier(_message.Message):
    __slots__ = ("id", "name", "initial_margin_ppm", "maintenance_fraction_ppm", "base_position_notional", "impact_notional")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INITIAL_MARGIN_PPM_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FRACTION_PPM_FIELD_NUMBER: _ClassVar[int]
    BASE_POSITION_NOTIONAL_FIELD_NUMBER: _ClassVar[int]
    IMPACT_NOTIONAL_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    initial_margin_ppm: int
    maintenance_fraction_ppm: int
    base_position_notional: int
    impact_notional: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., initial_margin_ppm: _Optional[int] = ..., maintenance_fraction_ppm: _Optional[int] = ..., base_position_notional: _Optional[int] = ..., impact_notional: _Optional[int] = ...) -> None: ...
