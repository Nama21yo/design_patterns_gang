# Client Streaming RPC

This folder demonstrates a client-streaming gRPC call: the client sends many request messages, then the server returns one final response after the client closes the stream.

The local server listens on `127.0.0.1:50053`.

## Files

- `sensor.proto`: streamed request, final response, and service contract.
- `server.py`: consumes the incoming request iterator and returns one average summary.
- `client.py`: uses a Python generator to stream sensor readings.
- `justfile`: compile and run commands.

## Commands

```zsh
just setup
just compile
just server
just client
just client-readings "20,21,24,25"
```

## Live Demo Flow

Terminal 1:

```zsh
cd client-streaming
just server
```

Terminal 2:

```zsh
cd client-streaming
just client
```

The server receives readings as the client yields them, but it sends only one `AverageResponse` after the client generator is exhausted.
