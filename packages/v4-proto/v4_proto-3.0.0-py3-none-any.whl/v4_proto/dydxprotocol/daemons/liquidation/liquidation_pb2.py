# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/daemons/liquidation/liquidation.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.subaccounts import subaccount_pb2 as dydxprotocol_dot_subaccounts_dot_subaccount__pb2
from v4_proto.dydxprotocol.clob import liquidations_pb2 as dydxprotocol_dot_clob_dot_liquidations__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n2dydxprotocol/daemons/liquidation/liquidation.proto\x12 dydxprotocol.daemons.liquidation\x1a\x14gogoproto/gogo.proto\x1a)dydxprotocol/subaccounts/subaccount.proto\x1a$dydxprotocol/clob/liquidations.proto\"\xb5\x02\n\x1bLiquidateSubaccountsRequest\x12\x14\n\x0c\x62lock_height\x18\x01 \x01(\r\x12Q\n\x1bliquidatable_subaccount_ids\x18\x02 \x03(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12Q\n\x1bnegative_tnc_subaccount_ids\x18\x03 \x03(\x0b\x32&.dydxprotocol.subaccounts.SubaccountIdB\x04\xc8\xde\x1f\x00\x12Z\n\x1dsubaccount_open_position_info\x18\x04 \x03(\x0b\x32-.dydxprotocol.clob.SubaccountOpenPositionInfoB\x04\xc8\xde\x1f\x00\"\x1e\n\x1cLiquidateSubaccountsResponse2\xac\x01\n\x12LiquidationService\x12\x95\x01\n\x14LiquidateSubaccounts\x12=.dydxprotocol.daemons.liquidation.LiquidateSubaccountsRequest\x1a>.dydxprotocol.daemons.liquidation.LiquidateSubaccountsResponseBCZAgithub.com/dydxprotocol/v4-chain/protocol/daemons/liquidation/apib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.daemons.liquidation.liquidation_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'ZAgithub.com/dydxprotocol/v4-chain/protocol/daemons/liquidation/api'
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['liquidatable_subaccount_ids']._options = None
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['liquidatable_subaccount_ids']._serialized_options = b'\310\336\037\000'
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['negative_tnc_subaccount_ids']._options = None
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['negative_tnc_subaccount_ids']._serialized_options = b'\310\336\037\000'
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['subaccount_open_position_info']._options = None
  _globals['_LIQUIDATESUBACCOUNTSREQUEST'].fields_by_name['subaccount_open_position_info']._serialized_options = b'\310\336\037\000'
  _globals['_LIQUIDATESUBACCOUNTSREQUEST']._serialized_start=192
  _globals['_LIQUIDATESUBACCOUNTSREQUEST']._serialized_end=501
  _globals['_LIQUIDATESUBACCOUNTSRESPONSE']._serialized_start=503
  _globals['_LIQUIDATESUBACCOUNTSRESPONSE']._serialized_end=533
  _globals['_LIQUIDATIONSERVICE']._serialized_start=536
  _globals['_LIQUIDATIONSERVICE']._serialized_end=708
# @@protoc_insertion_point(module_scope)
