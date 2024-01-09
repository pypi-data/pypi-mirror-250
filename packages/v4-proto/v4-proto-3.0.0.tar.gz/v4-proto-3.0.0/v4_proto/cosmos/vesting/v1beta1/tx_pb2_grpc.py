# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from v4_proto.cosmos.vesting.v1beta1 import tx_pb2 as cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2


class MsgStub(object):
    """Msg defines the bank Msg service.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateVestingAccount = channel.unary_unary(
                '/cosmos.vesting.v1beta1.Msg/CreateVestingAccount',
                request_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccount.SerializeToString,
                response_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccountResponse.FromString,
                )
        self.CreatePermanentLockedAccount = channel.unary_unary(
                '/cosmos.vesting.v1beta1.Msg/CreatePermanentLockedAccount',
                request_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccount.SerializeToString,
                response_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccountResponse.FromString,
                )
        self.CreatePeriodicVestingAccount = channel.unary_unary(
                '/cosmos.vesting.v1beta1.Msg/CreatePeriodicVestingAccount',
                request_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccount.SerializeToString,
                response_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccountResponse.FromString,
                )


class MsgServicer(object):
    """Msg defines the bank Msg service.
    """

    def CreateVestingAccount(self, request, context):
        """CreateVestingAccount defines a method that enables creating a vesting
        account.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreatePermanentLockedAccount(self, request, context):
        """CreatePermanentLockedAccount defines a method that enables creating a permanent
        locked account.

        Since: cosmos-sdk 0.46
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreatePeriodicVestingAccount(self, request, context):
        """CreatePeriodicVestingAccount defines a method that enables creating a
        periodic vesting account.

        Since: cosmos-sdk 0.46
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MsgServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateVestingAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateVestingAccount,
                    request_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccount.FromString,
                    response_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccountResponse.SerializeToString,
            ),
            'CreatePermanentLockedAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePermanentLockedAccount,
                    request_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccount.FromString,
                    response_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccountResponse.SerializeToString,
            ),
            'CreatePeriodicVestingAccount': grpc.unary_unary_rpc_method_handler(
                    servicer.CreatePeriodicVestingAccount,
                    request_deserializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccount.FromString,
                    response_serializer=cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccountResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'cosmos.vesting.v1beta1.Msg', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Msg(object):
    """Msg defines the bank Msg service.
    """

    @staticmethod
    def CreateVestingAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.vesting.v1beta1.Msg/CreateVestingAccount',
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccount.SerializeToString,
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreateVestingAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreatePermanentLockedAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.vesting.v1beta1.Msg/CreatePermanentLockedAccount',
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccount.SerializeToString,
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePermanentLockedAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreatePeriodicVestingAccount(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/cosmos.vesting.v1beta1.Msg/CreatePeriodicVestingAccount',
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccount.SerializeToString,
            cosmos_dot_vesting_dot_v1beta1_dot_tx__pb2.MsgCreatePeriodicVestingAccountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
