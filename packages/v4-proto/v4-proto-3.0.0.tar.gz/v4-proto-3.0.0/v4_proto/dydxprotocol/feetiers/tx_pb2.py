# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/feetiers/tx.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from v4_proto.dydxprotocol.feetiers import params_pb2 as dydxprotocol_dot_feetiers_dot_params__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x64ydxprotocol/feetiers/tx.proto\x12\x15\x64ydxprotocol.feetiers\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x17\x63osmos/msg/v1/msg.proto\x1a\"dydxprotocol/feetiers/params.proto\x1a\x14gogoproto/gogo.proto\"\x9b\x01\n\x1bMsgUpdatePerpetualFeeParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12?\n\x06params\x18\x02 \x01(\x0b\x32).dydxprotocol.feetiers.PerpetualFeeParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority\"%\n#MsgUpdatePerpetualFeeParamsResponse2\x92\x01\n\x03Msg\x12\x8a\x01\n\x18UpdatePerpetualFeeParams\x12\x32.dydxprotocol.feetiers.MsgUpdatePerpetualFeeParams\x1a:.dydxprotocol.feetiers.MsgUpdatePerpetualFeeParamsResponseB<Z:github.com/dydxprotocol/v4-chain/protocol/x/feetiers/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.feetiers.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z:github.com/dydxprotocol/v4-chain/protocol/x/feetiers/types'
  _globals['_MSGUPDATEPERPETUALFEEPARAMS'].fields_by_name['authority']._options = None
  _globals['_MSGUPDATEPERPETUALFEEPARAMS'].fields_by_name['authority']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGUPDATEPERPETUALFEEPARAMS'].fields_by_name['params']._options = None
  _globals['_MSGUPDATEPERPETUALFEEPARAMS'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_MSGUPDATEPERPETUALFEEPARAMS']._options = None
  _globals['_MSGUPDATEPERPETUALFEEPARAMS']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_MSGUPDATEPERPETUALFEEPARAMS']._serialized_start=168
  _globals['_MSGUPDATEPERPETUALFEEPARAMS']._serialized_end=323
  _globals['_MSGUPDATEPERPETUALFEEPARAMSRESPONSE']._serialized_start=325
  _globals['_MSGUPDATEPERPETUALFEEPARAMSRESPONSE']._serialized_end=362
  _globals['_MSG']._serialized_start=365
  _globals['_MSG']._serialized_end=511
# @@protoc_insertion_point(module_scope)
