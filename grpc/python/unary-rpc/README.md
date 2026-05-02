# Unary RPC

This folder demonstrates the simplest gRPC shape: one request from the client and one response from the server.

The local server listens on `127.0.0.1:50051`.

## Files

- `unary.proto`: request, response, and service contract.
- `server.py`: implements the generated `GreeterServicer`.
- `client.py`: creates a channel, builds a stub, sends `HelloRequest`, and receives `HelloReply`.
- `justfile`: compile and run commands.

## Commands

```zsh
just setup
just compile
just server
just client
just client-name "Matania"
```

## Live Demo Flow

Terminal 1:

```zsh
cd unary-rpc
just server
```

Terminal 2:

```zsh
cd unary-rpc
just client
```

The client calls `SayHello` as if it were a local Python method, while gRPC handles the HTTP/2 transport and protobuf serialization.
