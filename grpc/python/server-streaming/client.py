from __future__ import annotations

import sys

import grpc

import streaming_pb2
import streaming_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50052"
DEFAULT_LIMIT = 10


def parse_limit(argv: list[str]) -> int:
    if len(argv) == 1:
        return DEFAULT_LIMIT

    try:
        return int(argv[1])
    except ValueError as exc:
        raise SystemExit("limit must be an integer") from exc


def run(limit: int = DEFAULT_LIMIT) -> None:
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = streaming_pb2_grpc.NumberGeneratorStub(channel)

        request = streaming_pb2.NumberRequest(limit=limit)
        print(f"Waiting for server to stream {limit} numbers...")

        response_iterator = stub.GenerateNumbers(request)
        for response in response_iterator:
            print(f"Received: {response.result} | Info: {response.message}")

    print("\nStream closed by server.")


if __name__ == "__main__":
    run(parse_limit(sys.argv))
