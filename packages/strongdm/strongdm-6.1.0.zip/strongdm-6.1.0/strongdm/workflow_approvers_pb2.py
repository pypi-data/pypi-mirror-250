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
# source: workflow_approvers.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import options_pb2 as options__pb2
from . import spec_pb2 as spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18workflow_approvers.proto\x12\x02v1\x1a\roptions.proto\x1a\nspec.proto\"\x92\x01\n\x1eWorkflowApproversCreateRequest\x12\'\n\x04meta\x18\x01 \x01(\x0b\x32\x19.v1.CreateRequestMetadata\x12;\n\x11workflow_approver\x18\x02 \x01(\x0b\x32\x14.v1.WorkflowApproverB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:\n\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\"\xed\x01\n\x1fWorkflowApproversCreateResponse\x12(\n\x04meta\x18\x01 \x01(\x0b\x32\x1a.v1.CreateResponseMetadata\x12;\n\x11workflow_approver\x18\x02 \x01(\x0b\x32\x14.v1.WorkflowApproverB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:\n\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\"Z\n\x1aWorkflowApproverGetRequest\x12$\n\x04meta\x18\x01 \x01(\x0b\x32\x16.v1.GetRequestMetadata\x12\x16\n\x02id\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\"\xf2\x01\n\x1bWorkflowApproverGetResponse\x12\x31\n\x04meta\x18\x01 \x01(\x0b\x32\x17.v1.GetResponseMetadataB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12;\n\x11workflow_approver\x18\x02 \x01(\x0b\x32\x14.v1.WorkflowApproverB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:\n\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\"m\n\x1eWorkflowApproversDeleteRequest\x12\'\n\x04meta\x18\x01 \x01(\x0b\x32\x19.v1.DeleteRequestMetadata\x12\x16\n\x02id\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:\n\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\"\xb0\x01\n\x1fWorkflowApproversDeleteResponse\x12(\n\x04meta\x18\x01 \x01(\x0b\x32\x1a.v1.DeleteResponseMetadata\x12W\n\nrate_limit\x18\x02 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:\n\xfa\xf8\xb3\x07\x05\xa8\xf3\xb3\x07\x01\"s\n\x1cWorkflowApproversListRequest\x12%\n\x04meta\x18\x01 \x01(\x0b\x32\x17.v1.ListRequestMetadata\x12\x1a\n\x06\x66ilter\x18\x02 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:\x10\xfa\xf8\xb3\x07\x0b\xa8\xf3\xb3\x07\x01\xd2\xf3\xb3\x07\x01*\"\xf0\x01\n\x1dWorkflowApproversListResponse\x12&\n\x04meta\x18\x01 \x01(\x0b\x32\x18.v1.ListResponseMetadata\x12<\n\x12workflow_approvers\x18\x02 \x03(\x0b\x32\x14.v1.WorkflowApproverB\n\xf2\xf8\xb3\x07\x05\xb8\xf3\xb3\x07\x01\x12W\n\nrate_limit\x18\x03 \x01(\x0b\x32\x15.v1.RateLimitMetadataB,\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\xf2\xf8\xb3\x07\x06\xb2\xf4\xb3\x07\x01*\xf2\xf8\xb3\x07\x12\xb2\xf4\xb3\x07\r!json_gateway:\x10\xfa\xf8\xb3\x07\x0b\xa8\xf3\xb3\x07\x01\xd2\xf3\xb3\x07\x01*\"\x85\x02\n\x10WorkflowApprover\x12\x16\n\x02id\x18\x01 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12$\n\x0bworkflow_id\x18\x02 \x01(\tB\x0f\xf2\xf8\xb3\x07\n\xb0\xf3\xb3\x07\x01\xc0\xf3\xb3\x07\x01\x12\x1e\n\naccount_id\x18\x03 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01\x12\x1b\n\x07role_id\x18\x04 \x01(\tB\n\xf2\xf8\xb3\x07\x05\xb0\xf3\xb3\x07\x01:v\xfa\xf8\xb3\x07q\xa8\xf3\xb3\x07\x01\xc2\xf3\xb3\x07\x61\xa2\xf3\xb3\x07*tf_examples/workflow_approver_resource.txt\xaa\xf3\xb3\x07-tf_examples/workflow_approver_data_source.txt\xd2\xf3\xb3\x07\x01*2\xbd\x04\n\x11WorkflowApprovers\x12\x81\x01\n\x06\x43reate\x12\".v1.WorkflowApproversCreateRequest\x1a#.v1.WorkflowApproversCreateResponse\".\x82\xf9\xb3\x07\t\xa2\xf3\xb3\x07\x04post\x82\xf9\xb3\x07\x1b\xaa\xf3\xb3\x07\x16/v1/workflow-approvers\x12y\n\x03Get\x12\x1e.v1.WorkflowApproverGetRequest\x1a\x1f.v1.WorkflowApproverGetResponse\"1\x82\xf9\xb3\x07\x08\xa2\xf3\xb3\x07\x03get\x82\xf9\xb3\x07\x1f\xaa\xf3\xb3\x07\x1a/v1/workflow-approver/{id}\x12\x83\x01\n\x06\x44\x65lete\x12\".v1.WorkflowApproversDeleteRequest\x1a#.v1.WorkflowApproversDeleteResponse\"0\x82\xf9\xb3\x07\x0b\xa2\xf3\xb3\x07\x06\x64\x65lete\x82\xf9\xb3\x07\x1b\xaa\xf3\xb3\x07\x16/v1/workflow-approvers\x12z\n\x04List\x12 .v1.WorkflowApproversListRequest\x1a!.v1.WorkflowApproversListResponse\"-\x82\xf9\xb3\x07\x08\xa2\xf3\xb3\x07\x03get\x82\xf9\xb3\x07\x1b\xaa\xf3\xb3\x07\x16/v1/workflow-approvers\x1a\'\xca\xf9\xb3\x07\x15\xc2\xf9\xb3\x07\x10WorkflowApprover\xca\xf9\xb3\x07\x08\xd2\xf9\xb3\x07\x03nt-Bm\n\x19\x63om.strongdm.api.plumbingB\x19WorkflowApproversPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1b\x06proto3')



_WORKFLOWAPPROVERSCREATEREQUEST = DESCRIPTOR.message_types_by_name['WorkflowApproversCreateRequest']
_WORKFLOWAPPROVERSCREATERESPONSE = DESCRIPTOR.message_types_by_name['WorkflowApproversCreateResponse']
_WORKFLOWAPPROVERGETREQUEST = DESCRIPTOR.message_types_by_name['WorkflowApproverGetRequest']
_WORKFLOWAPPROVERGETRESPONSE = DESCRIPTOR.message_types_by_name['WorkflowApproverGetResponse']
_WORKFLOWAPPROVERSDELETEREQUEST = DESCRIPTOR.message_types_by_name['WorkflowApproversDeleteRequest']
_WORKFLOWAPPROVERSDELETERESPONSE = DESCRIPTOR.message_types_by_name['WorkflowApproversDeleteResponse']
_WORKFLOWAPPROVERSLISTREQUEST = DESCRIPTOR.message_types_by_name['WorkflowApproversListRequest']
_WORKFLOWAPPROVERSLISTRESPONSE = DESCRIPTOR.message_types_by_name['WorkflowApproversListResponse']
_WORKFLOWAPPROVER = DESCRIPTOR.message_types_by_name['WorkflowApprover']
WorkflowApproversCreateRequest = _reflection.GeneratedProtocolMessageType('WorkflowApproversCreateRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSCREATEREQUEST,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversCreateRequest)
  })
_sym_db.RegisterMessage(WorkflowApproversCreateRequest)

WorkflowApproversCreateResponse = _reflection.GeneratedProtocolMessageType('WorkflowApproversCreateResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSCREATERESPONSE,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversCreateResponse)
  })
_sym_db.RegisterMessage(WorkflowApproversCreateResponse)

WorkflowApproverGetRequest = _reflection.GeneratedProtocolMessageType('WorkflowApproverGetRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERGETREQUEST,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproverGetRequest)
  })
_sym_db.RegisterMessage(WorkflowApproverGetRequest)

WorkflowApproverGetResponse = _reflection.GeneratedProtocolMessageType('WorkflowApproverGetResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERGETRESPONSE,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproverGetResponse)
  })
_sym_db.RegisterMessage(WorkflowApproverGetResponse)

WorkflowApproversDeleteRequest = _reflection.GeneratedProtocolMessageType('WorkflowApproversDeleteRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSDELETEREQUEST,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversDeleteRequest)
  })
_sym_db.RegisterMessage(WorkflowApproversDeleteRequest)

WorkflowApproversDeleteResponse = _reflection.GeneratedProtocolMessageType('WorkflowApproversDeleteResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSDELETERESPONSE,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversDeleteResponse)
  })
_sym_db.RegisterMessage(WorkflowApproversDeleteResponse)

WorkflowApproversListRequest = _reflection.GeneratedProtocolMessageType('WorkflowApproversListRequest', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSLISTREQUEST,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversListRequest)
  })
_sym_db.RegisterMessage(WorkflowApproversListRequest)

WorkflowApproversListResponse = _reflection.GeneratedProtocolMessageType('WorkflowApproversListResponse', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVERSLISTRESPONSE,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApproversListResponse)
  })
_sym_db.RegisterMessage(WorkflowApproversListResponse)

WorkflowApprover = _reflection.GeneratedProtocolMessageType('WorkflowApprover', (_message.Message,), {
  'DESCRIPTOR' : _WORKFLOWAPPROVER,
  '__module__' : 'workflow_approvers_pb2'
  # @@protoc_insertion_point(class_scope:v1.WorkflowApprover)
  })
_sym_db.RegisterMessage(WorkflowApprover)

_WORKFLOWAPPROVERS = DESCRIPTOR.services_by_name['WorkflowApprovers']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\031com.strongdm.api.plumbingB\031WorkflowApproversPlumbingZ5github.com/strongdm/strongdm-sdk-go/v3/internal/v1;v1'
  _WORKFLOWAPPROVERSCREATEREQUEST.fields_by_name['workflow_approver']._options = None
  _WORKFLOWAPPROVERSCREATEREQUEST.fields_by_name['workflow_approver']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERSCREATEREQUEST._options = None
  _WORKFLOWAPPROVERSCREATEREQUEST._serialized_options = b'\372\370\263\007\005\250\363\263\007\001'
  _WORKFLOWAPPROVERSCREATERESPONSE.fields_by_name['workflow_approver']._options = None
  _WORKFLOWAPPROVERSCREATERESPONSE.fields_by_name['workflow_approver']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERSCREATERESPONSE.fields_by_name['rate_limit']._options = None
  _WORKFLOWAPPROVERSCREATERESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _WORKFLOWAPPROVERSCREATERESPONSE._options = None
  _WORKFLOWAPPROVERSCREATERESPONSE._serialized_options = b'\372\370\263\007\005\250\363\263\007\001'
  _WORKFLOWAPPROVERGETREQUEST.fields_by_name['id']._options = None
  _WORKFLOWAPPROVERGETREQUEST.fields_by_name['id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['meta']._options = None
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['meta']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['workflow_approver']._options = None
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['workflow_approver']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['rate_limit']._options = None
  _WORKFLOWAPPROVERGETRESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _WORKFLOWAPPROVERGETRESPONSE._options = None
  _WORKFLOWAPPROVERGETRESPONSE._serialized_options = b'\372\370\263\007\005\250\363\263\007\001'
  _WORKFLOWAPPROVERSDELETEREQUEST.fields_by_name['id']._options = None
  _WORKFLOWAPPROVERSDELETEREQUEST.fields_by_name['id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERSDELETEREQUEST._options = None
  _WORKFLOWAPPROVERSDELETEREQUEST._serialized_options = b'\372\370\263\007\005\250\363\263\007\001'
  _WORKFLOWAPPROVERSDELETERESPONSE.fields_by_name['rate_limit']._options = None
  _WORKFLOWAPPROVERSDELETERESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _WORKFLOWAPPROVERSDELETERESPONSE._options = None
  _WORKFLOWAPPROVERSDELETERESPONSE._serialized_options = b'\372\370\263\007\005\250\363\263\007\001'
  _WORKFLOWAPPROVERSLISTREQUEST.fields_by_name['filter']._options = None
  _WORKFLOWAPPROVERSLISTREQUEST.fields_by_name['filter']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVERSLISTREQUEST._options = None
  _WORKFLOWAPPROVERSLISTREQUEST._serialized_options = b'\372\370\263\007\013\250\363\263\007\001\322\363\263\007\001*'
  _WORKFLOWAPPROVERSLISTRESPONSE.fields_by_name['workflow_approvers']._options = None
  _WORKFLOWAPPROVERSLISTRESPONSE.fields_by_name['workflow_approvers']._serialized_options = b'\362\370\263\007\005\270\363\263\007\001'
  _WORKFLOWAPPROVERSLISTRESPONSE.fields_by_name['rate_limit']._options = None
  _WORKFLOWAPPROVERSLISTRESPONSE.fields_by_name['rate_limit']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001\362\370\263\007\006\262\364\263\007\001*\362\370\263\007\022\262\364\263\007\r!json_gateway'
  _WORKFLOWAPPROVERSLISTRESPONSE._options = None
  _WORKFLOWAPPROVERSLISTRESPONSE._serialized_options = b'\372\370\263\007\013\250\363\263\007\001\322\363\263\007\001*'
  _WORKFLOWAPPROVER.fields_by_name['id']._options = None
  _WORKFLOWAPPROVER.fields_by_name['id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVER.fields_by_name['workflow_id']._options = None
  _WORKFLOWAPPROVER.fields_by_name['workflow_id']._serialized_options = b'\362\370\263\007\n\260\363\263\007\001\300\363\263\007\001'
  _WORKFLOWAPPROVER.fields_by_name['account_id']._options = None
  _WORKFLOWAPPROVER.fields_by_name['account_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVER.fields_by_name['role_id']._options = None
  _WORKFLOWAPPROVER.fields_by_name['role_id']._serialized_options = b'\362\370\263\007\005\260\363\263\007\001'
  _WORKFLOWAPPROVER._options = None
  _WORKFLOWAPPROVER._serialized_options = b'\372\370\263\007q\250\363\263\007\001\302\363\263\007a\242\363\263\007*tf_examples/workflow_approver_resource.txt\252\363\263\007-tf_examples/workflow_approver_data_source.txt\322\363\263\007\001*'
  _WORKFLOWAPPROVERS._options = None
  _WORKFLOWAPPROVERS._serialized_options = b'\312\371\263\007\025\302\371\263\007\020WorkflowApprover\312\371\263\007\010\322\371\263\007\003nt-'
  _WORKFLOWAPPROVERS.methods_by_name['Create']._options = None
  _WORKFLOWAPPROVERS.methods_by_name['Create']._serialized_options = b'\202\371\263\007\t\242\363\263\007\004post\202\371\263\007\033\252\363\263\007\026/v1/workflow-approvers'
  _WORKFLOWAPPROVERS.methods_by_name['Get']._options = None
  _WORKFLOWAPPROVERS.methods_by_name['Get']._serialized_options = b'\202\371\263\007\010\242\363\263\007\003get\202\371\263\007\037\252\363\263\007\032/v1/workflow-approver/{id}'
  _WORKFLOWAPPROVERS.methods_by_name['Delete']._options = None
  _WORKFLOWAPPROVERS.methods_by_name['Delete']._serialized_options = b'\202\371\263\007\013\242\363\263\007\006delete\202\371\263\007\033\252\363\263\007\026/v1/workflow-approvers'
  _WORKFLOWAPPROVERS.methods_by_name['List']._options = None
  _WORKFLOWAPPROVERS.methods_by_name['List']._serialized_options = b'\202\371\263\007\010\242\363\263\007\003get\202\371\263\007\033\252\363\263\007\026/v1/workflow-approvers'
  _WORKFLOWAPPROVERSCREATEREQUEST._serialized_start=60
  _WORKFLOWAPPROVERSCREATEREQUEST._serialized_end=206
  _WORKFLOWAPPROVERSCREATERESPONSE._serialized_start=209
  _WORKFLOWAPPROVERSCREATERESPONSE._serialized_end=446
  _WORKFLOWAPPROVERGETREQUEST._serialized_start=448
  _WORKFLOWAPPROVERGETREQUEST._serialized_end=538
  _WORKFLOWAPPROVERGETRESPONSE._serialized_start=541
  _WORKFLOWAPPROVERGETRESPONSE._serialized_end=783
  _WORKFLOWAPPROVERSDELETEREQUEST._serialized_start=785
  _WORKFLOWAPPROVERSDELETEREQUEST._serialized_end=894
  _WORKFLOWAPPROVERSDELETERESPONSE._serialized_start=897
  _WORKFLOWAPPROVERSDELETERESPONSE._serialized_end=1073
  _WORKFLOWAPPROVERSLISTREQUEST._serialized_start=1075
  _WORKFLOWAPPROVERSLISTREQUEST._serialized_end=1190
  _WORKFLOWAPPROVERSLISTRESPONSE._serialized_start=1193
  _WORKFLOWAPPROVERSLISTRESPONSE._serialized_end=1433
  _WORKFLOWAPPROVER._serialized_start=1436
  _WORKFLOWAPPROVER._serialized_end=1697
  _WORKFLOWAPPROVERS._serialized_start=1700
  _WORKFLOWAPPROVERS._serialized_end=2273
# @@protoc_insertion_point(module_scope)
