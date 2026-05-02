from __future__ import annotations

from concurrent import futures
import time

import grpc

import streaming_pb2
import streaming_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50052"
STREAM_DELAY_SECONDS = 0.5


class NumberGeneratorService(streaming_pb2_grpc.NumberGeneratorServicer):
    def GenerateNumbers(
        self,
        request: streaming_pb2.NumberRequest,
        context: grpc.ServicerContext,
    ):
        print(f"[Server] Client requested {request.limit} numbers.")

        if request.limit < 1:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "limit must be greater than zero")

        for number in range(1, request.limit + 1):
            time.sleep(STREAM_DELAY_SECONDS)
            print(f"[Server] Yielding number: {number}")

            yield streaming_pb2.NumberResponse(
                result=number,
                message=f"Sending chunk {number} of {request.limit}",
            )

        print("[Server] Finished streaming all numbers.")


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_NumberGeneratorServicer_to_server(NumberGeneratorService(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print(f"Server-streaming server is running on {SERVER_ADDRESS}.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
