# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/mint/v1beta1/genesis.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.cosmos.mint.v1beta1 import mint_pb2 as cosmos_dot_mint_dot_v1beta1_dot_mint__pb2
from v4_proto.amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!cosmos/mint/v1beta1/genesis.proto\x12\x13\x63osmos.mint.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1e\x63osmos/mint/v1beta1/mint.proto\x1a\x11\x61mino/amino.proto\"~\n\x0cGenesisState\x12\x36\n\x06minter\x18\x01 \x01(\x0b\x32\x1b.cosmos.mint.v1beta1.MinterB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12\x36\n\x06params\x18\x02 \x01(\x0b\x32\x1b.cosmos.mint.v1beta1.ParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x42+Z)github.com/cosmos/cosmos-sdk/x/mint/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.mint.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z)github.com/cosmos/cosmos-sdk/x/mint/types'
  _globals['_GENESISSTATE'].fields_by_name['minter']._options = None
  _globals['_GENESISSTATE'].fields_by_name['minter']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['params']._options = None
  _globals['_GENESISSTATE'].fields_by_name['params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_GENESISSTATE']._serialized_start=131
  _globals['_GENESISSTATE']._serialized_end=257
# @@protoc_insertion_point(module_scope)
