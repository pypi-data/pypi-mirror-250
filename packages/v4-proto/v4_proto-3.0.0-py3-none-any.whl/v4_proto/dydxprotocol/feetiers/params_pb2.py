# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/feetiers/params.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\"dydxprotocol/feetiers/params.proto\x12\x15\x64ydxprotocol.feetiers\"L\n\x12PerpetualFeeParams\x12\x36\n\x05tiers\x18\x01 \x03(\x0b\x32\'.dydxprotocol.feetiers.PerpetualFeeTier\"\xcb\x01\n\x10PerpetualFeeTier\x12\x0c\n\x04name\x18\x01 \x01(\t\x12#\n\x1b\x61\x62solute_volume_requirement\x18\x02 \x01(\x04\x12*\n\"total_volume_share_requirement_ppm\x18\x03 \x01(\r\x12*\n\"maker_volume_share_requirement_ppm\x18\x04 \x01(\r\x12\x15\n\rmaker_fee_ppm\x18\x05 \x01(\x11\x12\x15\n\rtaker_fee_ppm\x18\x06 \x01(\x11\x42<Z:github.com/dydxprotocol/v4-chain/protocol/x/feetiers/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.feetiers.params_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z:github.com/dydxprotocol/v4-chain/protocol/x/feetiers/types'
  _globals['_PERPETUALFEEPARAMS']._serialized_start=61
  _globals['_PERPETUALFEEPARAMS']._serialized_end=137
  _globals['_PERPETUALFEETIER']._serialized_start=140
  _globals['_PERPETUALFEETIER']._serialized_end=343
# @@protoc_insertion_point(module_scope)
