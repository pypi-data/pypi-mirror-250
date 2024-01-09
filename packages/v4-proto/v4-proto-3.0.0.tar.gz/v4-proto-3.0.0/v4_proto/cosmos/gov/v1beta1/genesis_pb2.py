# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cosmos/gov/v1beta1/genesis.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from v4_proto.gogoproto import gogo_pb2 as gogoproto_dot_gogo__pb2
from v4_proto.cosmos.gov.v1beta1 import gov_pb2 as cosmos_dot_gov_dot_v1beta1_dot_gov__pb2
from v4_proto.amino import amino_pb2 as amino_dot_amino__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n cosmos/gov/v1beta1/genesis.proto\x12\x12\x63osmos.gov.v1beta1\x1a\x14gogoproto/gogo.proto\x1a\x1c\x63osmos/gov/v1beta1/gov.proto\x1a\x11\x61mino/amino.proto\"\xc4\x03\n\x0cGenesisState\x12\x1c\n\x14starting_proposal_id\x18\x01 \x01(\x04\x12\x44\n\x08\x64\x65posits\x18\x02 \x03(\x0b\x32\x1b.cosmos.gov.v1beta1.DepositB\x15\xc8\xde\x1f\x00\xaa\xdf\x1f\x08\x44\x65posits\xa8\xe7\xb0*\x01\x12;\n\x05votes\x18\x03 \x03(\x0b\x32\x18.cosmos.gov.v1beta1.VoteB\x12\xc8\xde\x1f\x00\xaa\xdf\x1f\x05Votes\xa8\xe7\xb0*\x01\x12G\n\tproposals\x18\x04 \x03(\x0b\x32\x1c.cosmos.gov.v1beta1.ProposalB\x16\xc8\xde\x1f\x00\xaa\xdf\x1f\tProposals\xa8\xe7\xb0*\x01\x12\x44\n\x0e\x64\x65posit_params\x18\x05 \x01(\x0b\x32!.cosmos.gov.v1beta1.DepositParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12\x42\n\rvoting_params\x18\x06 \x01(\x0b\x32 .cosmos.gov.v1beta1.VotingParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x12@\n\x0ctally_params\x18\x07 \x01(\x0b\x32\x1f.cosmos.gov.v1beta1.TallyParamsB\t\xc8\xde\x1f\x00\xa8\xe7\xb0*\x01\x42\x32Z0github.com/cosmos/cosmos-sdk/x/gov/types/v1beta1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cosmos.gov.v1beta1.genesis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z0github.com/cosmos/cosmos-sdk/x/gov/types/v1beta1'
  _globals['_GENESISSTATE'].fields_by_name['deposits']._options = None
  _globals['_GENESISSTATE'].fields_by_name['deposits']._serialized_options = b'\310\336\037\000\252\337\037\010Deposits\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['votes']._options = None
  _globals['_GENESISSTATE'].fields_by_name['votes']._serialized_options = b'\310\336\037\000\252\337\037\005Votes\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['proposals']._options = None
  _globals['_GENESISSTATE'].fields_by_name['proposals']._serialized_options = b'\310\336\037\000\252\337\037\tProposals\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['deposit_params']._options = None
  _globals['_GENESISSTATE'].fields_by_name['deposit_params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['voting_params']._options = None
  _globals['_GENESISSTATE'].fields_by_name['voting_params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_GENESISSTATE'].fields_by_name['tally_params']._options = None
  _globals['_GENESISSTATE'].fields_by_name['tally_params']._serialized_options = b'\310\336\037\000\250\347\260*\001'
  _globals['_GENESISSTATE']._serialized_start=128
  _globals['_GENESISSTATE']._serialized_end=580
# @@protoc_insertion_point(module_scope)
