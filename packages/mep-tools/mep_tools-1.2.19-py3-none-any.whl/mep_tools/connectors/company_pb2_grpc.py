# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import company_pb2 as company__pb2


class CompanyServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Get = channel.unary_unary(
                '/connector.company.CompanyService/Get',
                request_serializer=company__pb2.CompanyGetRequest.SerializeToString,
                response_deserializer=company__pb2.CompanyResponse.FromString,
                )
        self.Create = channel.unary_unary(
                '/connector.company.CompanyService/Create',
                request_serializer=company__pb2.CompanyCreateRequest.SerializeToString,
                response_deserializer=company__pb2.CompanyResponse.FromString,
                )
        self.Update = channel.unary_unary(
                '/connector.company.CompanyService/Update',
                request_serializer=company__pb2.CompanyUpdateRequest.SerializeToString,
                response_deserializer=company__pb2.CompanyResponse.FromString,
                )


class CompanyServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Get(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Create(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Update(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CompanyServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Get': grpc.unary_unary_rpc_method_handler(
                    servicer.Get,
                    request_deserializer=company__pb2.CompanyGetRequest.FromString,
                    response_serializer=company__pb2.CompanyResponse.SerializeToString,
            ),
            'Create': grpc.unary_unary_rpc_method_handler(
                    servicer.Create,
                    request_deserializer=company__pb2.CompanyCreateRequest.FromString,
                    response_serializer=company__pb2.CompanyResponse.SerializeToString,
            ),
            'Update': grpc.unary_unary_rpc_method_handler(
                    servicer.Update,
                    request_deserializer=company__pb2.CompanyUpdateRequest.FromString,
                    response_serializer=company__pb2.CompanyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'connector.company.CompanyService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class CompanyService(object):
    """Missing associated documentation comment in .proto file."""

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
        return grpc.experimental.unary_unary(request, target, '/connector.company.CompanyService/Get',
            company__pb2.CompanyGetRequest.SerializeToString,
            company__pb2.CompanyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

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
        return grpc.experimental.unary_unary(request, target, '/connector.company.CompanyService/Create',
            company__pb2.CompanyCreateRequest.SerializeToString,
            company__pb2.CompanyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Update(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/connector.company.CompanyService/Update',
            company__pb2.CompanyUpdateRequest.SerializeToString,
            company__pb2.CompanyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
