# Channel Sharing And Thread Safety

This folder demonstrates how a gRPC channel can be shared safely across stubs and worker threads.

It uses the Unary Greeter service from `../unary-rpc/unary.proto` and calls the Unary server at `127.0.0.1:50051`.

## What This Proves

- One channel can be reused instead of creating a new channel for every RPC.
- Multiple stubs can share the same channel.
- One stub and channel can be used concurrently from multiple Python threads.

## Commands

Terminal 1:

```zsh
cd unary-rpc
just server
```

Terminal 2:

```zsh
cd channels
just client
just client-workers 10
```

The server will receive one warmup request from `SharedChannelWarmup`, then multiple concurrent requests named `WorkerThread-0`, `WorkerThread-1`, and so on.
