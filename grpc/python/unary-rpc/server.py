from concurrent import futures

import grpc

import unary_pb2
import unary_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50051"


class GreeterService(unary_pb2_grpc.GreeterServicer):
    def SayHello(self, request: unary_pb2.HelloRequest, context: grpc.ServicerContext) -> unary_pb2.HelloReply:
        print(f"[Server] Received a request from: {request.name}")
        greeting = f"Hello there, {request.name}! Welcome to gRPC."
        return unary_pb2.HelloReply(message=greeting)


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    unary_pb2_grpc.add_GreeterServicer_to_server(GreeterService(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print(f"Server is running on {SERVER_ADDRESS}.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
