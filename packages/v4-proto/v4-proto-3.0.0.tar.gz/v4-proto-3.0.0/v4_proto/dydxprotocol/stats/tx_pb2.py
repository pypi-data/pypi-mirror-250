# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/stats/tx.proto
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
from v4_proto.dydxprotocol.stats import params_pb2 as dydxprotocol_dot_stats_dot_params__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1b\x64ydxprotocol/stats/tx.proto\x12\x12\x64ydxprotocol.stats\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x17\x63osmos/msg/v1/msg.proto\x1a\x1f\x64ydxprotocol/stats/params.proto\x1a\x14gogoproto/gogo.proto\"\x80\x01\n\x0fMsgUpdateParams\x12+\n\tauthority\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x30\n\x06params\x18\x02 \x01(\x0b\x32\x1a.dydxprotocol.stats.ParamsB\x04\xc8\xde\x1f\x00:\x0e\x82\xe7\xb0*\tauthority\"\x19\n\x17MsgUpdateParamsResponse2g\n\x03Msg\x12`\n\x0cUpdateParams\x12#.dydxprotocol.stats.MsgUpdateParams\x1a+.dydxprotocol.stats.MsgUpdateParamsResponseB9Z7github.com/dydxprotocol/v4-chain/protocol/x/stats/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.stats.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/dydxprotocol/v4-chain/protocol/x/stats/types'
  _globals['_MSGUPDATEPARAMS'].fields_by_name['authority']._options = None
  _globals['_MSGUPDATEPARAMS'].fields_by_name['authority']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_MSGUPDATEPARAMS'].fields_by_name['params']._options = None
  _globals['_MSGUPDATEPARAMS'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_MSGUPDATEPARAMS']._options = None
  _globals['_MSGUPDATEPARAMS']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_MSGUPDATEPARAMS']._serialized_start=159
  _globals['_MSGUPDATEPARAMS']._serialized_end=287
  _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_start=289
  _globals['_MSGUPDATEPARAMSRESPONSE']._serialized_end=314
  _globals['_MSG']._serialized_start=316
  _globals['_MSG']._serialized_end=419
# @@protoc_insertion_point(module_scope)
