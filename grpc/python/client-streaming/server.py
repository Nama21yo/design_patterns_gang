from __future__ import annotations

from concurrent import futures

import grpc

import sensor_pb2
import sensor_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50053"


class DataProcessorService(sensor_pb2_grpc.DataProcessorServicer):
    def ComputeAverage(
        self,
        request_iterator,
        context: grpc.ServicerContext,
    ) -> sensor_pb2.AverageResponse:
        print("[Server] Receiving sensor stream...")

        total_temp = 0
        count = 0

        for reading in request_iterator:
            print(f"[Server] Received temperature: {reading.temperature} C")
            total_temp += reading.temperature
            count += 1

        average = total_temp / count if count else 0
        print(f"[Server] Stream closed by client. Calculated average: {average:.2f} C")

        return sensor_pb2.AverageResponse(
            average_temp=average,
            total_readings=count,
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_DataProcessorServicer_to_server(DataProcessorService(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print(f"Client-streaming server is running on {SERVER_ADDRESS}.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
