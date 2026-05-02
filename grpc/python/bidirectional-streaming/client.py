from __future__ import annotations

import sys
import time
from collections.abc import Iterator

import grpc

import chat_pb2
import chat_pb2_grpc


SERVER_ADDRESS = "127.0.0.1:50054"
DEFAULT_USER = "Alice"
DEFAULT_MESSAGES = [
    "Hi! Are you there?",
    "Can you help me with my account?",
    "Nevermind, I figured it out.",
    "Thanks anyway, goodbye!",
]
MESSAGE_DELAY_SECONDS = 1.0


def generate_chat_messages(user: str) -> Iterator[chat_pb2.ChatMessage]:
    for message in DEFAULT_MESSAGES:
        print(f"\n[Client] Sending: {message}")
        yield chat_pb2.ChatMessage(user=user, text=message)
        time.sleep(MESSAGE_DELAY_SECONDS)


def run(user: str = DEFAULT_USER) -> None:
    with grpc.insecure_channel(SERVER_ADDRESS) as channel:
        grpc.channel_ready_future(channel).result(timeout=5)
        stub = chat_pb2_grpc.ChatServiceStub(channel)

        print("Connecting to live chat...")
        response_iterator = stub.LiveChat(generate_chat_messages(user))

        for response in response_iterator:
            print(f"[{response.user}]: {response.text}")

    print("\nDisconnected from chat.")


if __name__ == "__main__":
    request_user = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_USER
    run(request_user)
