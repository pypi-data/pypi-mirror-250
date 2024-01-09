# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/stats/stats.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1e\x64ydxprotocol/stats/stats.proto\x12\x12\x64ydxprotocol.stats\x1a\x14gogoproto/gogo.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"x\n\nBlockStats\x12\x32\n\x05\x66ills\x18\x01 \x03(\x0b\x32#.dydxprotocol.stats.BlockStats.Fill\x1a\x36\n\x04\x46ill\x12\r\n\x05taker\x18\x01 \x01(\t\x12\r\n\x05maker\x18\x02 \x01(\t\x12\x10\n\x08notional\x18\x03 \x01(\x04\"\'\n\rStatsMetadata\x12\x16\n\x0etrailing_epoch\x18\x01 \x01(\r\"\xd4\x01\n\nEpochStats\x12<\n\x0e\x65poch_end_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x08\xc8\xde\x1f\x00\x90\xdf\x1f\x01\x12;\n\x05stats\x18\x02 \x03(\x0b\x32,.dydxprotocol.stats.EpochStats.UserWithStats\x1aK\n\rUserWithStats\x12\x0c\n\x04user\x18\x01 \x01(\t\x12,\n\x05stats\x18\x02 \x01(\x0b\x32\x1d.dydxprotocol.stats.UserStats\"&\n\x0bGlobalStats\x12\x17\n\x0fnotional_traded\x18\x01 \x01(\x04\";\n\tUserStats\x12\x16\n\x0etaker_notional\x18\x01 \x01(\x04\x12\x16\n\x0emaker_notional\x18\x02 \x01(\x04\x42\x39Z7github.com/dydxprotocol/v4-chain/protocol/x/stats/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.stats.stats_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z7github.com/dydxprotocol/v4-chain/protocol/x/stats/types'
  _globals['_EPOCHSTATS'].fields_by_name['epoch_end_time']._options = None
  _globals['_EPOCHSTATS'].fields_by_name['epoch_end_time']._serialized_options = b'\310\336\037\000\220\337\037\001'
  _globals['_BLOCKSTATS']._serialized_start=109
  _globals['_BLOCKSTATS']._serialized_end=229
  _globals['_BLOCKSTATS_FILL']._serialized_start=175
  _globals['_BLOCKSTATS_FILL']._serialized_end=229
  _globals['_STATSMETADATA']._serialized_start=231
  _globals['_STATSMETADATA']._serialized_end=270
  _globals['_EPOCHSTATS']._serialized_start=273
  _globals['_EPOCHSTATS']._serialized_end=485
  _globals['_EPOCHSTATS_USERWITHSTATS']._serialized_start=410
  _globals['_EPOCHSTATS_USERWITHSTATS']._serialized_end=485
  _globals['_GLOBALSTATS']._serialized_start=487
  _globals['_GLOBALSTATS']._serialized_end=525
  _globals['_USERSTATS']._serialized_start=527
  _globals['_USERSTATS']._serialized_end=586
# @@protoc_insertion_point(module_scope)
