# Protocol Buffers Playground

This directory is a lecture playground for understanding Protocol Buffers before moving into gRPC services.

The runnable protobuf implementation lives in `protobuf/`. The unary RPC implementation lives in `unary-rpc/`. The server-streaming implementation lives in `server-streaming/`. The client-streaming implementation lives in `client-streaming/`. The bidirectional-streaming implementation lives in `bidirectional-streaming/`. The channel-sharing implementation lives in `channels/`. The load-balancing implementation lives in `load-balancing/`. The virtual environment lives in this `python/` folder.

## Setup

```zsh
uv venv
source .venv/bin/activate
uv pip install grpcio grpcio-tools protobuf
```

Or use the `justfile`:

```zsh
cd protobuf
just setup
source ../.venv/bin/activate
```

## Files

- `protobuf/address.proto`: a small reusable message.
- `protobuf/person.proto`: imports, package, options, enum, repeated fields, map fields, oneof, and wrapper fields.
- `protobuf/person_v2.proto`: a versioning example using `reserved`.
- `protobuf/main.py`: Python code that constructs, compares, serializes, deserializes, and inspects protobuf messages.
- `unary-rpc/unary.proto`: a unary gRPC service contract.
- `unary-rpc/server.py`: unary gRPC server implementation.
- `unary-rpc/client.py`: unary gRPC client implementation.
- `server-streaming/streaming.proto`: a server-streaming gRPC service contract.
- `server-streaming/server.py`: server-streaming gRPC server implementation.
- `server-streaming/client.py`: server-streaming gRPC client implementation.
- `client-streaming/sensor.proto`: a client-streaming gRPC service contract.
- `client-streaming/server.py`: client-streaming gRPC server implementation.
- `client-streaming/client.py`: client-streaming gRPC client implementation.
- `bidirectional-streaming/chat.proto`: a bidirectional-streaming gRPC service contract.
- `bidirectional-streaming/server.py`: bidirectional-streaming gRPC server implementation.
- `bidirectional-streaming/client.py`: bidirectional-streaming gRPC client implementation.
- `channels/advanced_client.py`: shared-channel and thread-safety client demo using the Unary Greeter service.
- `load-balancing/lb.proto`: load-balanced unary gRPC service contract.
- `load-balancing/server.py`: backend server that reports which port handled the request.
- `load-balancing/client.py`: client that sends repeated requests through Nginx.
- `load-balancing/nginx.conf`: Nginx gRPC reverse-proxy configuration.

## Commands

```zsh
cd protobuf
just compile
just run
just hexdump
just clean
```

## Lecture Flow

1. Start with `address.proto` and explain package names and numeric tags.
2. Move to `person.proto` and explain each protobuf feature from top to bottom.
3. Run `just compile` and show the generated `*_pb2.py` files.
4. Run `just run` and connect the Python API to the proto definitions.
5. Run `just hexdump` and show that field names are absent from the binary payload.
6. Use `person_v2.proto` to explain safe schema evolution.
