# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/blocktime/genesis.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.blocktime import params_pb2 as dydxprotocol_dot_blocktime_dot_params__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$dydxprotocol/blocktime/genesis.proto\x12\x16\x64ydxprotocol.blocktime\x1a\x14gogoproto/gogo.proto\x1a#dydxprotocol/blocktime/params.proto\"L\n\x0cGenesisState\x12<\n\x06params\x18\x01 \x01(\x0b\x32&.dydxprotocol.blocktime.DowntimeParamsB\x04\xc8\xde\x1f\x00\x42=Z;github.com/dydxprotocol/v4-chain/protocol/x/blocktime/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.blocktime.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z;github.com/dydxprotocol/v4-chain/protocol/x/blocktime/types'
  _globals['_GENESISSTATE'].fields_by_name['params']._options = None
  _globals['_GENESISSTATE'].fields_by_name['params']._serialized_options = b'\310\336\037\000'
  _globals['_GENESISSTATE']._serialized_start=123
  _globals['_GENESISSTATE']._serialized_end=199
# @@protoc_insertion_point(module_scope)
