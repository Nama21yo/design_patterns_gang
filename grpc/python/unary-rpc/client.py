from __future__ import annotations

import sys

import grpc

import unary_pb2
import unary_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50051"


def run(name: str = "Engineering Students") -> None:
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = unary_pb2_grpc.GreeterStub(channel)

        print("Creating the request...")
        request = unary_pb2.HelloRequest(name=name)

        print("Calling SayHello on the server...")
        response = stub.SayHello(request)

    print(f"\nServer replied: {response.message}")


if __name__ == "__main__":
    request_name = sys.argv[1] if len(sys.argv) > 1 else "Engineering Students"
    run(request_name)
