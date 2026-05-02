# Bidirectional Streaming RPC

This folder demonstrates a bidirectional-streaming gRPC call: the client streams messages to the server, and the server streams messages back over the same RPC.

The local server listens on `127.0.0.1:50054`.

## Files

- `chat.proto`: shared chat message and duplex service contract.
- `server.py`: receives a request iterator and yields streamed replies.
- `client.py`: sends messages with a generator and iterates over server replies.
- `justfile`: compile and run commands.

## Commands

```zsh
just setup
just compile
just server
just client
just client-user "Bob"
```

## Live Demo Flow

Terminal 1:

```zsh
cd bidirectional-streaming
just server
```

Terminal 2:

```zsh
cd bidirectional-streaming
just client
```

Both sides keep the RPC open. The client sends one chat message at a time, and the server replies on the response stream without waiting for the whole client stream to finish.
