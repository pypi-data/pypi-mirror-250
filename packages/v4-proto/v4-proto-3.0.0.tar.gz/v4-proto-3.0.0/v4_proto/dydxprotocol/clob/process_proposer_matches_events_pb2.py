# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dydxprotocol/clob/process_proposer_matches_events.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.dydxprotocol.clob import order_pb2 as dydxprotocol_dot_clob_dot_order__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n7dydxprotocol/clob/process_proposer_matches_events.proto\x12\x11\x64ydxprotocol.clob\x1a\x14gogoproto/gogo.proto\x1a\x1d\x64ydxprotocol/clob/order.proto\"\xc3\x04\n\x1cProcessProposerMatchesEvents\x12\x44\n\x1aplaced_long_term_order_ids\x18\x01 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12\x44\n\x1a\x65xpired_stateful_order_ids\x18\x02 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12H\n\x1eorder_ids_filled_in_last_block\x18\x03 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12P\n&placed_stateful_cancellation_order_ids\x18\x04 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12\x44\n\x1aremoved_stateful_order_ids\x18\x05 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12W\n-conditional_order_ids_triggered_in_last_block\x18\x06 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12\x46\n\x1cplaced_conditional_order_ids\x18\x07 \x03(\x0b\x32\x1a.dydxprotocol.clob.OrderIdB\x04\xc8\xde\x1f\x00\x12\x14\n\x0c\x62lock_height\x18\x08 \x01(\rB8Z6github.com/dydxprotocol/v4-chain/protocol/x/clob/typesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dydxprotocol.clob.process_proposer_matches_events_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z6github.com/dydxprotocol/v4-chain/protocol/x/clob/types'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_long_term_order_ids']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_long_term_order_ids']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['expired_stateful_order_ids']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['expired_stateful_order_ids']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['order_ids_filled_in_last_block']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['order_ids_filled_in_last_block']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_stateful_cancellation_order_ids']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_stateful_cancellation_order_ids']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['removed_stateful_order_ids']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['removed_stateful_order_ids']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['conditional_order_ids_triggered_in_last_block']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['conditional_order_ids_triggered_in_last_block']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_conditional_order_ids']._options = None
  _globals['_PROCESSPROPOSERMATCHESEVENTS'].fields_by_name['placed_conditional_order_ids']._serialized_options = b'\310\336\037\000'
  _globals['_PROCESSPROPOSERMATCHESEVENTS']._serialized_start=132
  _globals['_PROCESSPROPOSERMATCHESEVENTS']._serialized_end=711
# @@protoc_insertion_point(module_scope)
