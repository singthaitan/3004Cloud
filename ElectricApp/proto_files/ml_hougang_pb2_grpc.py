# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from proto_files import ml_hougang_pb2 as proto__files_dot_ml__hougang__pb2


class ml_HougangStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetUsageData = channel.unary_unary(
                '/ml_hougang.ml_Hougang/GetUsageData',
                request_serializer=proto__files_dot_ml__hougang__pb2.UsageData_Request.SerializeToString,
                response_deserializer=proto__files_dot_ml__hougang__pb2.UsageData_Reply.FromString,
                )
        self.GetPredictionData = channel.unary_unary(
                '/ml_hougang.ml_Hougang/GetPredictionData',
                request_serializer=proto__files_dot_ml__hougang__pb2.PredictionData_Request.SerializeToString,
                response_deserializer=proto__files_dot_ml__hougang__pb2.PredictionData_Reply.FromString,
                )


class ml_HougangServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetUsageData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPredictionData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ml_HougangServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetUsageData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUsageData,
                    request_deserializer=proto__files_dot_ml__hougang__pb2.UsageData_Request.FromString,
                    response_serializer=proto__files_dot_ml__hougang__pb2.UsageData_Reply.SerializeToString,
            ),
            'GetPredictionData': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPredictionData,
                    request_deserializer=proto__files_dot_ml__hougang__pb2.PredictionData_Request.FromString,
                    response_serializer=proto__files_dot_ml__hougang__pb2.PredictionData_Reply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ml_hougang.ml_Hougang', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ml_Hougang(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetUsageData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ml_hougang.ml_Hougang/GetUsageData',
            proto__files_dot_ml__hougang__pb2.UsageData_Request.SerializeToString,
            proto__files_dot_ml__hougang__pb2.UsageData_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetPredictionData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ml_hougang.ml_Hougang/GetPredictionData',
            proto__files_dot_ml__hougang__pb2.PredictionData_Request.SerializeToString,
            proto__files_dot_ml__hougang__pb2.PredictionData_Reply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
