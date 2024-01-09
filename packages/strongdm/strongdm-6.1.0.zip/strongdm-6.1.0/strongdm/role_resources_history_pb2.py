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
# source: role_resources_history.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import role_resources_pb2 as role__resources__pb2
from . import options_pb2 as options__pb2
from . import spec_pb2 as spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1crole_resources_history.proto\x12\x02v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x14role_resources.proto\x1a\roptions.proto\x1a\nspec.proto\"\x8d\x01\n\x1eRoleResourceHistoryListRequest\x12%\n\x04meta\x18\x01 \x01(\x0b\x32\x17.v1.ListRequestMetadata\x12\x1a\n\x06\x66ilter\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\x82\x02\n\x1fRoleResourceHistoryListResponse\x12&\n\x04meta\x18\x01 \x01(\x0b\x32\x18.v1.ListResponseMetadata\x12\x34\n\x07history\x18\x02 \x03(\x0b\x32\x17.v1.RoleResourceHistoryB\n\xf2\xf8\xb3\x07\x05\xb8\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\x96\x02\n\x13RoleResourceHistory\x12\x1f\n\x0b\x61\x63tivity_id\x18\x01 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12\x39\n\ttimestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12\x33\n\rrole_resource\x18\x03 \x01(\x0b\x32\x10.v1.RoleResourceB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12:\n\ndeleted_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:2\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider2\xec\x01\n\x14RoleResourcesHistory\x12\x82\x01\n\x04List\x12\".v1.RoleResourceHistoryListRequest\x1a#.v1.RoleResourceHistoryListResponse\"1\x82\xf9\xb3\x07\x08\xa2\xf3\xb3\x07\x03get\x82\xf9\xb3\x07\x1f\xaa\xf3\xb3\x07\x1a/v1/role-resources-history\x1aO\xca\xf9\xb3\x07\x18\xc2\xf9\xb3\x07\x13RoleResourceHistory\xca\xf9\xb3\x07\x05\xd8\xf9\xb3\x07\x01\xca\xf9\xb3\x07\x06\xca\xf9\xb3\x07\x01*\xca\xf9\xb3\x07\x18\xca\xf9\xb3\x07\x13!terraform-providerB\x98\x01\n\x19\x63om.strongdm.api.plumbingB\x1cRoleResourcesHistoryPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\xc2\x92\xb4\x07\x06\xa2\x8c\xb4\x07\x01*\xc2\x92\xb4\x07\x18\xa2\x8c\xb4\x07\x13!terraform-providerb\x06proto3')



_ROLERESOURCEHISTORYLISTREQUEST = DESCRIPTOR.message_types_by_name['RoleResourceHistoryListRequest']
_ROLERESOURCEHISTORYLISTRESPONSE = DESCRIPTOR.message_types_by_name['RoleResourceHistoryListResponse']
_ROLERESOURCEHISTORY = DESCRIPTOR.message_types_by_name['RoleResourceHistory']
RoleResourceHistoryListRequest = _reflection.GeneratedProtocolMessageType('RoleResourceHistoryListRequest', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCEHISTORYLISTREQUEST,
  '__module__' : 'role_resources_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResourceHistoryListRequest)
  })
_sym_db.RegisterMessage(RoleResourceHistoryListRequest)

RoleResourceHistoryListResponse = _reflection.GeneratedProtocolMessageType('RoleResourceHistoryListResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCEHISTORYLISTRESPONSE,
  '__module__' : 'role_resources_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResourceHistoryListResponse)
  })
_sym_db.RegisterMessage(RoleResourceHistoryListResponse)

RoleResourceHistory = _reflection.GeneratedProtocolMessageType('RoleResourceHistory', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCEHISTORY,
  '__module__' : 'role_resources_history_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResourceHistory)
  })
_sym_db.RegisterMessage(RoleResourceHistory)

_ROLERESOURCESHISTORY = DESCRIPTOR.services_by_name['RoleResourcesHistory']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.strongdm.api.plumbingB\034RoleResourcesHistoryPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\302\222\264\007\006\242\214\264\007\001*\302\222\264\007\030\242\214\264\007\023!terraform-provider'
  _ROLERESOURCEHISTORYLISTREQUEST.fields_by_name['filter']._options = None
  _ROLERESOURCEHISTORYLISTREQUEST.fields_by_name['filter']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCEHISTORYLISTREQUEST._options = None
  _ROLERESOURCEHISTORYLISTREQUEST._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCEHISTORYLISTRESPONSE.fields_by_name['history']._options = None
  _ROLERESOURCEHISTORYLISTRESPONSE.fields_by_name['history']._serialized_options = b'\362\370\263\007\005\270\363\263\007\001'
  _ROLERESOURCEHISTORYLISTRESPONSE.fields_by_name['rate_limit']._options = None
  _ROLERESOURCEHISTORYLISTRESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _ROLERESOURCEHISTORYLISTRESPONSE._options = None
  _ROLERESOURCEHISTORYLISTRESPONSE._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCEHISTORY.fields_by_name['activity_id']._options = None
  _ROLERESOURCEHISTORY.fields_by_name['activity_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCEHISTORY.fields_by_name['timestamp']._options = None
  _ROLERESOURCEHISTORY.fields_by_name['timestamp']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCEHISTORY.fields_by_name['role_resource']._options = None
  _ROLERESOURCEHISTORY.fields_by_name['role_resource']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCEHISTORY.fields_by_name['deleted_at']._options = None
  _ROLERESOURCEHISTORY.fields_by_name['deleted_at']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCEHISTORY._options = None
  _ROLERESOURCEHISTORY._serialized_options = b'\372\370\263\007\005\250\363\263\007\001\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCESHISTORY._options = None
  _ROLERESOURCESHISTORY._serialized_options = b'\312\371\263\007\030\302\371\263\007\023RoleResourceHistory\312\371\263\007\005\330\371\263\007\001\312\371\263\007\006\312\371\263\007\001*\312\371\263\007\030\312\371\263\007\023!terraform-provider'
  _ROLERESOURCESHISTORY.methods_by_name['List']._options = None
  _ROLERESOURCESHISTORY.methods_by_name['List']._serialized_options = b'\202\371\263\007\010\242\363\263\007\003get\202\371\263\007\037\252\363\263\007\032/v1/role-resources-history'
  _ROLERESOURCEHISTORYLISTREQUEST._serialized_start=119
  _ROLERESOURCEHISTORYLISTREQUEST._serialized_end=260
  _ROLERESOURCEHISTORYLISTRESPONSE._serialized_start=263
  _ROLERESOURCEHISTORYLISTRESPONSE._serialized_end=521
  _ROLERESOURCEHISTORY._serialized_start=524
  _ROLERESOURCEHISTORY._serialized_end=802
  _ROLERESOURCESHISTORY._serialized_start=805
  _ROLERESOURCESHISTORY._serialized_end=1041
# @@protoc_insertion_point(module_scope)
