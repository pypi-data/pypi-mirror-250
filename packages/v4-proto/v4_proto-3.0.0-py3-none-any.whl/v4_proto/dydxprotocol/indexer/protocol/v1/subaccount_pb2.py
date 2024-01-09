# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/indexer/protocol/v1/subaccount.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.cosmos_proto import cosmos_pb2 as cosmos__proto_dot_cosmos__pb2
from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n1dydxprotocol/indexer/protocol/v1/subaccount.proto\x12 dydxprotocol.indexer.protocol.v1\x1a\x19\x63osmos_proto/cosmos.proto\x1a\x14gogoproto/gogo.proto\"N\n\x13IndexerSubaccountId\x12\'\n\x05owner\x18\x01 \x01(\tB\x18\xd2\xb4-\x14\x63osmos.AddressString\x12\x0e\n\x06number\x18\x02 \x01(\r\"\xd0\x02\n\x18IndexerPerpetualPosition\x12\x14\n\x0cperpetual_id\x18\x01 \x01(\r\x12Z\n\x08quantums\x18\x02 \x01(\x0c\x42H\xc8\xde\x1f\x00\xda\xde\x1f@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt\x12_\n\rfunding_index\x18\x03 \x01(\x0c\x42H\xc8\xde\x1f\x00\xda\xde\x1f@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt\x12\x61\n\x0f\x66unding_payment\x18\x04 \x01(\x0c\x42H\xc8\xde\x1f\x00\xda\xde\x1f@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt\"\x93\x01\n\x14IndexerAssetPosition\x12\x10\n\x08\x61sset_id\x18\x01 \x01(\r\x12Z\n\x08quantums\x18\x02 \x01(\x0c\x42H\xc8\xde\x1f\x00\xda\xde\x1f@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt\x12\r\n\x05index\x18\x03 \x01(\x04\x42?Z=github.com/dydxprotocol/v4-chain/protocol/indexer/protocol/v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.indexer.protocol.v1.subaccount_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z=github.com/dydxprotocol/v4-chain/protocol/indexer/protocol/v1'
  _globals['_INDEXERSUBACCOUNTID'].fields_by_name['owner']._options = None
  _globals['_INDEXERSUBACCOUNTID'].fields_by_name['owner']._serialized_options = b'\322\264-\024cosmos.AddressString'
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['quantums']._options = None
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['quantums']._serialized_options = b'\310\336\037\000\332\336\037@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt'
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['funding_index']._options = None
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['funding_index']._serialized_options = b'\310\336\037\000\332\336\037@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt'
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['funding_payment']._options = None
  _globals['_INDEXERPERPETUALPOSITION'].fields_by_name['funding_payment']._serialized_options = b'\310\336\037\000\332\336\037@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt'
  _globals['_INDEXERASSETPOSITION'].fields_by_name['quantums']._options = None
  _globals['_INDEXERASSETPOSITION'].fields_by_name['quantums']._serialized_options = b'\310\336\037\000\332\336\037@github.com/dydxprotocol/v4-chain/protocol/dtypes.SerializableInt'
  _globals['_INDEXERSUBACCOUNTID']._serialized_start=136
  _globals['_INDEXERSUBACCOUNTID']._serialized_end=214
  _globals['_INDEXERPERPETUALPOSITION']._serialized_start=217
  _globals['_INDEXERPERPETUALPOSITION']._serialized_end=553
  _globals['_INDEXERASSETPOSITION']._serialized_start=556
  _globals['_INDEXERASSETPOSITION']._serialized_end=703
# @@protoc_insertion_point(module_scope)
