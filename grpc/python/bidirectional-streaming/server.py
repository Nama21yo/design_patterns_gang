from __future__ import annotations

from concurrent import futures

import grpc

import chat_pb2
import chat_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50054"


class LiveChatService(chat_pb2_grpc.ChatServiceServicer):
    def LiveChat(
        self,
        request_iterator,
        context: grpc.ServicerContext,
    ):
        print("[Server] A new client joined the chat.")

        for incoming_message in request_iterator:
            print(f"[Server] Received from {incoming_message.user}: {incoming_message.text}")

            reply_text = (
                f"Hello {incoming_message.user}, "
                f"I heard you say: '{incoming_message.text}'"
            )

            yield chat_pb2.ChatMessage(
                user="ServerBot",
                text=reply_text,
            )

        print("[Server] The client left the chat.")


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(LiveChatService(), server)

    server.add_insecure_port(SERVER_ADDRESS)
    server.start()
    print(f"Bidirectional chat server is running on {SERVER_ADDRESS}.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nStopping server.")
        server.stop(grace=1)


if __name__ == "__main__":
    serve()
