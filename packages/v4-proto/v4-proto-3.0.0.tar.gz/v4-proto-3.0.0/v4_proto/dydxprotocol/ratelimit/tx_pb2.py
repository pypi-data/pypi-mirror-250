# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/ratelimit/tx.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos.msg.v1 import msg_pb2 as cosmos_dot_msg_dot_v1_dot_msg__pb2
from v4_proto.dydxprotocol.ratelimit import limit_params_pb2 as dydxprotocol_dot_ratelimit_dot_limit__params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1f\x64ydxprotocol/ratelimit/tx.proto\x12\x16\x64ydxprotocol.ratelimit\x1a\x17\x63osmos/msg/v1/msg.proto\x1a)dydxprotocol/ratelimit/limit_params.proto\"q\n\x11MsgSetLimitParams\x12\x11\n\tauthority\x18\x01 \x01(\t\x12\x39\n\x0climit_params\x18\x02 \x01(\x0b\x32#.dydxprotocol.ratelimit.LimitParams:\x0e\x82\xe7\xb0*\tauthority\"\x1b\n\x19MsgSetLimitParamsResponse\"H\n\x14MsgDeleteLimitParams\x12\x11\n\tauthority\x18\x01 \x01(\t\x12\r\n\x05\x64\x65nom\x18\x02 \x01(\t:\x0e\x82\xe7\xb0*\tauthority\"\x1e\n\x1cMsgDeleteLimitParamsResponse2\xee\x01\n\x03Msg\x12n\n\x0eSetLimitParams\x12).dydxprotocol.ratelimit.MsgSetLimitParams\x1a\x31.dydxprotocol.ratelimit.MsgSetLimitParamsResponse\x12w\n\x11\x44\x65leteLimitParams\x12,.dydxprotocol.ratelimit.MsgDeleteLimitParams\x1a\x34.dydxprotocol.ratelimit.MsgDeleteLimitParamsResponseB=Z;github.com/dydxprotocol/v4-chain/protocol/x/ratelimit/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.ratelimit.tx_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/dydxprotocol/v4-chain/protocol/x/ratelimit/types'
  _globals['_MSGSETLIMITPARAMS']._options = None
  _globals['_MSGSETLIMITPARAMS']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_MSGDELETELIMITPARAMS']._options = None
  _globals['_MSGDELETELIMITPARAMS']._serialized_options = b'\202\347\260*\tauthority'
  _globals['_MSGSETLIMITPARAMS']._serialized_start=127
  _globals['_MSGSETLIMITPARAMS']._serialized_end=240
  _globals['_MSGSETLIMITPARAMSRESPONSE']._serialized_start=242
  _globals['_MSGSETLIMITPARAMSRESPONSE']._serialized_end=269
  _globals['_MSGDELETELIMITPARAMS']._serialized_start=271
  _globals['_MSGDELETELIMITPARAMS']._serialized_end=343
  _globals['_MSGDELETELIMITPARAMSRESPONSE']._serialized_start=345
  _globals['_MSGDELETELIMITPARAMSRESPONSE']._serialized_end=375
  _globals['_MSG']._serialized_start=378
  _globals['_MSG']._serialized_end=616
# @@protoc_insertion_point(module_scope)
