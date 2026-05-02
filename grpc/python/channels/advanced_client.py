from __future__ import annotations

import sys
import time
from concurrent import futures

import grpc

import unary_pb2
import unary_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50051"
DEFAULT_WORKER_COUNT = 5


def parse_worker_count(argv: list[str]) -> int:
    if len(argv) == 1:
        return DEFAULT_WORKER_COUNT

    try:
        worker_count = int(argv[1])
    except ValueError as exc:
        raise SystemExit("worker count must be an integer") from exc

    if worker_count < 1:
        raise SystemExit("worker count must be greater than zero")

    return worker_count


def make_rpc_call(thread_id: int, stub: unary_pb2_grpc.GreeterStub) -> str:
    print(f"[Thread {thread_id}] Preparing to call server...")

    request = unary_pb2.HelloRequest(name=f"WorkerThread-{thread_id}")
    response = stub.SayHello(request, timeout=5)

    output = f"[Thread {thread_id}] Response: {response.message}"
    print(output)
    return output


def run(worker_count: int = DEFAULT_WORKER_COUNT) -> None:
    print("Initializing one shared channel.")

    with grpc.insecure_channel(SERVER_ADDRESS) as shared_channel:
        greeter_stub_1 = unary_pb2_grpc.GreeterStub(shared_channel)
        greeter_stub_2 = unary_pb2_grpc.GreeterStub(shared_channel)

        print(f"Shared channel object id: {id(shared_channel)}")
        print(f"Greeter stub 1 object id: {id(greeter_stub_1)}")
        print(f"Greeter stub 2 object id: {id(greeter_stub_2)}")
        print("Two stubs now share the same channel. No RPC has been made yet.")
        time.sleep(1)

        print("\nCalling once through stub 2 to prove a second stub can use the same channel...")
        warmup_response = greeter_stub_2.SayHello(
            unary_pb2.HelloRequest(name="SharedChannelWarmup"),
            timeout=5,
        )
        print(f"[Warmup] Response: {warmup_response.message}")

        print(f"\nFiring {worker_count} concurrent calls using stub 1 and the same channel...")
        with futures.ThreadPoolExecutor(max_workers=worker_count) as executor:
            submitted_calls = [
                executor.submit(make_rpc_call, thread_id, greeter_stub_1)
                for thread_id in range(worker_count)
            ]

            for submitted_call in futures.as_completed(submitted_calls):
                submitted_call.result()

    print("\nAll threads finished. Shared channel closed cleanly.")


if __name__ == "__main__":
    run(parse_worker_count(sys.argv))
