from __future__ import annotations

import sys
import time
from collections.abc import Iterable, Iterator

import grpc

import sensor_pb2
import sensor_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50053"
DEFAULT_READINGS = [22, 24, 25, 23, 26, 28, 27]
STREAM_DELAY_SECONDS = 0.5


def parse_readings(argv: list[str]) -> list[int]:
    if len(argv) == 1:
        return DEFAULT_READINGS

    try:
        readings = [int(value.strip()) for value in argv[1].split(",") if value.strip()]
    except ValueError as exc:
        raise SystemExit("readings must be comma-separated integers") from exc

    if not readings:
        raise SystemExit("provide at least one reading")

    return readings


def generate_sensor_readings(readings: Iterable[int]) -> Iterator[sensor_pb2.SensorData]:
    for temperature in readings:
        print(f"[Client] Streaming reading to server: {temperature} C")
        yield sensor_pb2.SensorData(temperature=temperature)
        time.sleep(STREAM_DELAY_SECONDS)


def run(readings: list[int]) -> None:
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = sensor_pb2_grpc.DataProcessorStub(channel)

        print("Starting sensor stream...")
        response = stub.ComputeAverage(generate_sensor_readings(readings))

    print("\nStream finished. Server replied:")
    print(f"Total readings: {response.total_readings}")
    print(f"Average temp:   {response.average_temp:.2f} C")


if __name__ == "__main__":
    run(parse_readings(sys.argv))
