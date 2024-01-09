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
# source: role_resources.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from . import options_pb2 as options__pb2
from . import spec_pb2 as spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14role_resources.proto\x12\x02v1\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\roptions.proto\x1a\nspec.proto\"\x86\x01\n\x17RoleResourceListRequest\x12%\n\x04meta\x18\x01 \x01(\x0b\x32\x17.v1.ListRequestMetadata\x12\x1a\n\x06\x66ilter\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\xfb\x01\n\x18RoleResourceListResponse\x12&\n\x04meta\x18\x01 \x01(\x0b\x32\x18.v1.ListResponseMetadata\x12\x34\n\x0erole_resources\x18\x02 \x03(\x0b\x32\x10.v1.RoleResourceB\n\xf2\xf8\xb3\x07\x05\xb8\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:(\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider\"\xbc\x01\n\x0cRoleResource\x12\x1b\n\x07role_id\x18\x01 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12\x1f\n\x0bresource_id\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12:\n\ngranted_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:2\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\xfa\xf8\xb3\x07\x06\xd2\xf3\xb3\x07\x01*\xfa\xf8\xb3\x07\x18\xd2\xf3\xb3\x07\x13!terraform-provider2\xbd\x01\n\rRoleResources\x12l\n\x04List\x12\x1b.v1.RoleResourceListRequest\x1a\x1c.v1.RoleResourceListResponse\")\x82\xf9\xb3\x07\x08\xa2\xf3\xb3\x07\x03get\x82\xf9\xb3\x07\x17\xaa\xf3\xb3\x07\x12/v1/role-resources\x1a>\xca\xf9\xb3\x07\x11\xc2\xf9\xb3\x07\x0cRoleResource\xca\xf9\xb3\x07\x06\xca\xf9\xb3\x07\x01*\xca\xf9\xb3\x07\x18\xca\xf9\xb3\x07\x13!terraform-providerB\x91\x01\n\x19\x63om.strongdm.api.plumbingB\x15RoleResourcesPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\xc2\x92\xb4\x07\x06\xa2\x8c\xb4\x07\x01*\xc2\x92\xb4\x07\x18\xa2\x8c\xb4\x07\x13!terraform-providerb\x06proto3')



_ROLERESOURCELISTREQUEST = DESCRIPTOR.message_types_by_name['RoleResourceListRequest']
_ROLERESOURCELISTRESPONSE = DESCRIPTOR.message_types_by_name['RoleResourceListResponse']
_ROLERESOURCE = DESCRIPTOR.message_types_by_name['RoleResource']
RoleResourceListRequest = _reflection.GeneratedProtocolMessageType('RoleResourceListRequest', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCELISTREQUEST,
  '__module__' : 'role_resources_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResourceListRequest)
  })
_sym_db.RegisterMessage(RoleResourceListRequest)

RoleResourceListResponse = _reflection.GeneratedProtocolMessageType('RoleResourceListResponse', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCELISTRESPONSE,
  '__module__' : 'role_resources_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResourceListResponse)
  })
_sym_db.RegisterMessage(RoleResourceListResponse)

RoleResource = _reflection.GeneratedProtocolMessageType('RoleResource', (_message.Message,), {
  'DESCRIPTOR' : _ROLERESOURCE,
  '__module__' : 'role_resources_pb2'
  # @@protoc_insertion_point(class_scope:v1.RoleResource)
  })
_sym_db.RegisterMessage(RoleResource)

_ROLERESOURCES = DESCRIPTOR.services_by_name['RoleResources']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.strongdm.api.plumbingB\025RoleResourcesPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1\302\222\264\007\006\242\214\264\007\001*\302\222\264\007\030\242\214\264\007\023!terraform-provider'
  _ROLERESOURCELISTREQUEST.fields_by_name['filter']._options = None
  _ROLERESOURCELISTREQUEST.fields_by_name['filter']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCELISTREQUEST._options = None
  _ROLERESOURCELISTREQUEST._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCELISTRESPONSE.fields_by_name['role_resources']._options = None
  _ROLERESOURCELISTRESPONSE.fields_by_name['role_resources']._serialized_options = b'\362\370\263\007\005\270\363\263\007\001'
  _ROLERESOURCELISTRESPONSE.fields_by_name['rate_limit']._options = None
  _ROLERESOURCELISTRESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _ROLERESOURCELISTRESPONSE._options = None
  _ROLERESOURCELISTRESPONSE._serialized_options = b'\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCE.fields_by_name['role_id']._options = None
  _ROLERESOURCE.fields_by_name['role_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCE.fields_by_name['resource_id']._options = None
  _ROLERESOURCE.fields_by_name['resource_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCE.fields_by_name['granted_at']._options = None
  _ROLERESOURCE.fields_by_name['granted_at']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _ROLERESOURCE._options = None
  _ROLERESOURCE._serialized_options = b'\372\370\263\007\005\250\363\263\007\001\372\370\263\007\006\322\363\263\007\001*\372\370\263\007\030\322\363\263\007\023!terraform-provider'
  _ROLERESOURCES._options = None
  _ROLERESOURCES._serialized_options = b'\312\371\263\007\021\302\371\263\007\014RoleResource\312\371\263\007\006\312\371\263\007\001*\312\371\263\007\030\312\371\263\007\023!terraform-provider'
  _ROLERESOURCES.methods_by_name['List']._options = None
  _ROLERESOURCES.methods_by_name['List']._serialized_options = b'\202\371\263\007\010\242\363\263\007\003get\202\371\263\007\027\252\363\263\007\022/v1/role-resources'
  _ROLERESOURCELISTREQUEST._serialized_start=89
  _ROLERESOURCELISTREQUEST._serialized_end=223
  _ROLERESOURCELISTRESPONSE._serialized_start=226
  _ROLERESOURCELISTRESPONSE._serialized_end=477
  _ROLERESOURCE._serialized_start=480
  _ROLERESOURCE._serialized_end=668
  _ROLERESOURCES._serialized_start=671
  _ROLERESOURCES._serialized_end=860
# @@protoc_insertion_point(module_scope)
