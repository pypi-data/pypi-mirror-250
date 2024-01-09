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
# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import peering_groups_pb2 as peering__groups__pb2


class PeeringGroupsStub(object):
    """PeeringGroups provides the building blocks necessary to obtain explicit network topology and routing.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Create = channel.unary_unary(
                '/v1.PeeringGroups/Create',
                request_serializer=peering__groups__pb2.PeeringGroupCreateRequest.SerializeToString,
                response_deserializer=peering__groups__pb2.PeeringGroupCreateResponse.FromString,
                )
        self.Delete = channel.unary_unary(
                '/v1.PeeringGroups/Delete',
                request_serializer=peering__groups__pb2.PeeringGroupDeleteRequest.SerializeToString,
                response_deserializer=peering__groups__pb2.PeeringGroupDeleteResponse.FromString,
                )
        self.Get = channel.unary_unary(
                '/v1.PeeringGroups/Get',
                request_serializer=peering__groups__pb2.PeeringGroupGetRequest.SerializeToString,
                response_deserializer=peering__groups__pb2.PeeringGroupGetResponse.FromString,
                )
        self.List = channel.unary_unary(
                '/v1.PeeringGroups/List',
                request_serializer=peering__groups__pb2.PeeringGroupListRequest.SerializeToString,
                response_deserializer=peering__groups__pb2.PeeringGroupListResponse.FromString,
                )


class PeeringGroupsServicer(object):
    """PeeringGroups provides the building blocks necessary to obtain explicit network topology and routing.
    """

    def Create(self, request, context):
        """Create registers a new PeeringGroup.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Delete(self, request, context):
        """Delete removes a PeeringGroup by ID.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Get(self, request, context):
        """Get reads one PeeringGroup by ID. It will load all its dependencies.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """List gets a list of Peering Groups.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PeeringGroupsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=peering__groups__pb2.PeeringGroupCreateRequest.FromString,
                    response_serializer=peering__groups__pb2.PeeringGroupCreateResponse.SerializeToString,
            ),
            'Delete': grpc.unary_unary_rpc_method_handler(
                    servicer.Delete,
                    request_deserializer=peering__groups__pb2.PeeringGroupDeleteRequest.FromString,
                    response_serializer=peering__groups__pb2.PeeringGroupDeleteResponse.SerializeToString,
            ),
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=peering__groups__pb2.PeeringGroupGetRequest.FromString,
                    response_serializer=peering__groups__pb2.PeeringGroupGetResponse.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=peering__groups__pb2.PeeringGroupListRequest.FromString,
                    response_serializer=peering__groups__pb2.PeeringGroupListResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'v1.PeeringGroups', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PeeringGroups(object):
    """PeeringGroups provides the building blocks necessary to obtain explicit network topology and routing.
    """

    @staticmethod
    def Create(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/v1.PeeringGroups/Create',
            peering__groups__pb2.PeeringGroupCreateRequest.SerializeToString,
            peering__groups__pb2.PeeringGroupCreateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Delete(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/v1.PeeringGroups/Delete',
            peering__groups__pb2.PeeringGroupDeleteRequest.SerializeToString,
            peering__groups__pb2.PeeringGroupDeleteResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Get(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/v1.PeeringGroups/Get',
            peering__groups__pb2.PeeringGroupGetRequest.SerializeToString,
            peering__groups__pb2.PeeringGroupGetResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/v1.PeeringGroups/List',
            peering__groups__pb2.PeeringGroupListRequest.SerializeToString,
            peering__groups__pb2.PeeringGroupListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
