# Server Streaming RPC

This folder demonstrates a server-streaming gRPC call: the client sends one request, and the server sends many response messages over the same RPC.

The local server listens on `127.0.0.1:50052`.

## Files

- `streaming.proto`: request, streamed response, and service contract.
- `server.py`: implements `GenerateNumbers` with a Python generator.
- `client.py`: calls `GenerateNumbers` and iterates over streamed responses.
- `justfile`: compile and run commands.

## Commands

```zsh
just setup
just compile
just server
just client
just client-limit 5
```

## Live Demo Flow

Terminal 1:

```zsh
cd server-streaming
just server
```

Terminal 2:

```zsh
cd server-streaming
just client
```

The client starts printing as soon as the first `NumberResponse` arrives. It does not wait for the server to generate the whole sequence.
