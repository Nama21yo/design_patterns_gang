from __future__ import annotations

from concurrent import futures
import sys

import grpc

import lb_pb2
import lb_pb2_grpc


DEFAULT_PORT = "50061"


class PingService(lb_pb2_grpc.PingServiceServicer):
    def __init__(self, port: str) -> None:
        self.port = port

    def Ping(self, request: lb_pb2.PingRequest, context: grpc.ServicerContext) -> lb_pb2.PongResponse:
        print(f"[Server on {self.port}] Handled request from: {request.client_name}")
        return lb_pb2.PongResponse(server_id=f"Server running on port {self.port}")


def parse_port(argv: list[str]) -> str:
    if len(argv) == 1:
        return DEFAULT_PORT

    port = argv[1]
    if not port.isdigit():
        raise SystemExit("port must be numeric")

    return port


def serve(port: str) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lb_pb2_grpc.add_PingServiceServicer_to_server(PingService(port), server)

    server_address = f"127.0.0.1:{port}"
    server.add_insecure_port(server_address)
    server.start()
    print(f"Backend server started on {server_address}.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve(parse_port(sys.argv))
