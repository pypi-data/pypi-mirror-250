# Copyright 2020 StrongDM Inc
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: accounts_history.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import accounts_pb2 as accounts__pb2
from . import options_pb2 as options__pb2
from . import spec_pb2 as spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16\x61\x63\x63ounts_history.proto\x12\x02v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x0e\x61\x63\x63ounts.proto\x1a\roptions.proto\x1a\nspec.proto\"\x88\x01\n\x19\x41\x63\x63ountHistoryListRequest\x12%\n\x04meta\x18\x01 \x01(\x0b\x32\x17.v1.ListRequestMetadata\x12\x1a\n\x06\x66ilter\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\xf8\x01\n\x1a\x41\x63\x63ountHistoryListResponse\x12&\n\x04meta\x18\x01 \x01(\x0b\x32\x18.v1.ListResponseMetadata\x12/\n\x07history\x18\x02 \x03(\x0b\x32\x12.v1.AccountHistoryB\n\xf2\xf8\xb3\x07\x05\xb8\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\x86\x02\n\x0e\x41\x63\x63ountHistory\x12\x1f\n\x0b\x61\x63tivity_id\x18\x01 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12\x39\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12(\n\x07\x61\x63\x63ount\x18\x03 \x01(\x0b\x32\x0b.v1.AccountB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12:\n\ndeleted_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:2\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider2\xd1\x01\n\x0f\x41\x63\x63ountsHistory\x12r\n\x04List\x12\x1d.v1.AccountHistoryListRequest\x1a\x1e.v1.AccountHistoryListResponse\"+\x82\xf9\xb3\x07\x08\xa2\xf3\xb3\x07\x03get\x82\xf9\xb3\x07\x19\xaa\xf3\xb3\x07\x14/v1/accounts-history\x1aJ\xca\xf9\xb3\x07\x13\xc2\xf9\xb3\x07\x0e\x41\x63\x63ountHistory\xca\xf9\xb3\x07\x05\xd8\xf9\xb3\x07\x01\xca\xf9\xb3\x07\x06\xca\xf9\xb3\x07\x01*\xca\xf9\xb3\x07\x18\xca\xf9\xb3\x07\x13!terraform-providerB\x93\x01\n\x19\x63om.strongdm.api.plumbingB\x17\x41\x63\x63ountsHistoryPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\xc2\x92\xb4\x07\x06\xa2\x8c\xb4\x07\x01*\xc2\x92\xb4\x07\x18\xa2\x8c\xb4\x07\x13!terraform-providerb\x06proto3')



_ACCOUNTHISTORYLISTREQUEST = DESCRIPTOR.message_types_by_name['AccountHistoryListRequest']
_ACCOUNTHISTORYLISTRESPONSE = DESCRIPTOR.message_types_by_name['AccountHistoryListResponse']
_ACCOUNTHISTORY = DESCRIPTOR.message_types_by_name['AccountHistory']
AccountHistoryListRequest = _reflection.GeneratedProtocolMessageType('AccountHistoryListRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTHISTORYLISTREQUEST,
  '__module__' : 'accounts_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.AccountHistoryListRequest)
  })
_sym_db.RegisterMessage(AccountHistoryListRequest)

AccountHistoryListResponse = _reflection.GeneratedProtocolMessageType('AccountHistoryListResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTHISTORYLISTRESPONSE,
  '__module__' : 'accounts_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.AccountHistoryListResponse)
  })
_sym_db.RegisterMessage(AccountHistoryListResponse)

AccountHistory = _reflection.GeneratedProtocolMessageType('AccountHistory', (_message.Message,), {
  'DESCRIPTOR' : _ACCOUNTHISTORY,
  '__module__' : 'accounts_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.AccountHistory)
  })
_sym_db.RegisterMessage(AccountHistory)

_ACCOUNTSHISTORY = DESCRIPTOR.services_by_name['AccountsHistory']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.strongdm.api.plumbingB\027AccountsHistoryPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\302\222\264\007\006\242\214\264\007\001*\302\222\264\007\030\242\214\264\007\023!terraform-provider'
  _ACCOUNTHISTORYLISTREQUEST.fields_by_name['filter']._options = None
  _ACCOUNTHISTORYLISTREQUEST.fields_by_name['filter']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ACCOUNTHISTORYLISTREQUEST._options = None
  _ACCOUNTHISTORYLISTREQUEST._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ACCOUNTHISTORYLISTRESPONSE.fields_by_name['history']._options = None
  _ACCOUNTHISTORYLISTRESPONSE.fields_by_name['history']._serialized_options = b'\362\370\263\007\005\270\363\263\007\001'
  _ACCOUNTHISTORYLISTRESPONSE.fields_by_name['rate_limit']._options = None
  _ACCOUNTHISTORYLISTRESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _ACCOUNTHISTORYLISTRESPONSE._options = None
  _ACCOUNTHISTORYLISTRESPONSE._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ACCOUNTHISTORY.fields_by_name['activity_id']._options = None
  _ACCOUNTHISTORY.fields_by_name['activity_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ACCOUNTHISTORY.fields_by_name['timestamp']._options = None
  _ACCOUNTHISTORY.fields_by_name['timestamp']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ACCOUNTHISTORY.fields_by_name['account']._options = None
  _ACCOUNTHISTORY.fields_by_name['account']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ACCOUNTHISTORY.fields_by_name['deleted_at']._options = None
  _ACCOUNTHISTORY.fields_by_name['deleted_at']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ACCOUNTHISTORY._options = None
  _ACCOUNTHISTORY._serialized_options = b'\372\370\263\007\005\250\363\263\007\001\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ACCOUNTSHISTORY._options = None
  _ACCOUNTSHISTORY._serialized_options = b'\312\371\263\007\023\302\371\263\007\016AccountHistory\312\371\263\007\005\330\371\263\007\001\312\371\263\007\006\312\371\263\007\001*\312\371\263\007\030\312\371\263\007\023!terraform-provider'
  _ACCOUNTSHISTORY.methods_by_name['List']._options = None
  _ACCOUNTSHISTORY.methods_by_name['List']._serialized_options = b'\202\371\263\007\010\242\363\263\007\003get\202\371\263\007\031\252\363\263\007\024/v1/accounts-history'
  _ACCOUNTHISTORYLISTREQUEST._serialized_start=107
  _ACCOUNTHISTORYLISTREQUEST._serialized_end=243
  _ACCOUNTHISTORYLISTRESPONSE._serialized_start=246
  _ACCOUNTHISTORYLISTRESPONSE._serialized_end=494
  _ACCOUNTHISTORY._serialized_start=497
  _ACCOUNTHISTORY._serialized_end=759
  _ACCOUNTSHISTORY._serialized_start=762
  _ACCOUNTSHISTORY._serialized_end=971
# @@protoc_insertion_point(module_scope)
