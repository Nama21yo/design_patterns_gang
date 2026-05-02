from __future__ import annotations

import sys
import time

import grpc

import lb_pb2
import lb_pb2_grpc


LOAD_BALANCER_ADDRESS = "127.0.0.1:8080"
DEFAULT_REQUEST_COUNT = 10
REQUEST_DELAY_SECONDS = 0.5


def parse_request_count(argv: list[str]) -> int:
    if len(argv) == 1:
        return DEFAULT_REQUEST_COUNT

    try:
        request_count = int(argv[1])
    except ValueError as exc:
        raise SystemExit("request count must be an integer") from exc

    if request_count < 1:
        raise SystemExit("request count must be greater than zero")

    return request_count


def run(request_count: int = DEFAULT_REQUEST_COUNT) -> None:
    print(f"Connecting to Nginx load balancer on {LOAD_BALANCER_ADDRESS}...")

    with grpc.insecure_channel(LOAD_BALANCER_ADDRESS) as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = lb_pb2_grpc.PingServiceStub(channel)

        for request_number in range(1, request_count + 1):
            request = lb_pb2.PingRequest(client_name=f"Request #{request_number}")
            response = stub.Ping(request, timeout=5)
            print(f"Sent Request #{request_number} | Answered by: {response.server_id}")
            time.sleep(REQUEST_DELAY_SECONDS)


if __name__ == "__main__":
    run(parse_request_count(sys.argv))
