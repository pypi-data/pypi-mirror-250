# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from v4_proto.cosmos.store.streaming.abci import grpc_pb2 as cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2


class ABCIListenerServiceStub(object):
    """ABCIListenerService is the service for the BaseApp ABCIListener interface
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ListenFinalizeBlock = channel.unary_unary(
                '/cosmos.store.streaming.abci.ABCIListenerService/ListenFinalizeBlock',
                request_serializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockRequest.SerializeToString,
                response_deserializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockResponse.FromString,
                )
        self.ListenCommit = channel.unary_unary(
                '/cosmos.store.streaming.abci.ABCIListenerService/ListenCommit',
                request_serializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitRequest.SerializeToString,
                response_deserializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitResponse.FromString,
                )


class ABCIListenerServiceServicer(object):
    """ABCIListenerService is the service for the BaseApp ABCIListener interface
    """

    def ListenFinalizeBlock(self, request, context):
        """ListenFinalizeBlock is the corresponding endpoint for ABCIListener.ListenEndBlock
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListenCommit(self, request, context):
        """ListenCommit is the corresponding endpoint for ABCIListener.ListenCommit
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ABCIListenerServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ListenFinalizeBlock': grpc.unary_unary_rpc_method_handler(
                    servicer.ListenFinalizeBlock,
                    request_deserializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockRequest.FromString,
                    response_serializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockResponse.SerializeToString,
            ),
            'ListenCommit': grpc.unary_unary_rpc_method_handler(
                    servicer.ListenCommit,
                    request_deserializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitRequest.FromString,
                    response_serializer=cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.store.streaming.abci.ABCIListenerService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ABCIListenerService(object):
    """ABCIListenerService is the service for the BaseApp ABCIListener interface
    """

    @staticmethod
    def ListenFinalizeBlock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.store.streaming.abci.ABCIListenerService/ListenFinalizeBlock',
            cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockRequest.SerializeToString,
            cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenFinalizeBlockResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListenCommit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.store.streaming.abci.ABCIListenerService/ListenCommit',
            cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitRequest.SerializeToString,
            cosmos_dot_store_dot_streaming_dot_abci_dot_grpc__pb2.ListenCommitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
