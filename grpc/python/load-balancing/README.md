# gRPC Load Balancing With Nginx

This folder demonstrates server-side load balancing for gRPC with Nginx.

The client sends requests to Nginx at `127.0.0.1:8080`. Nginx forwards the gRPC calls to two backend Python servers:

- `127.0.0.1:50061`
- `127.0.0.1:50062`

Nginx uses round-robin balancing by default.

## Files

- `lb.proto`: request, response, and `PingService` contract.
- `server.py`: backend gRPC server. The port is passed on the command line.
- `client.py`: sends repeated requests to Nginx, not directly to the backend servers.
- `nginx.conf`: Nginx HTTP/2 plus `grpc_pass` reverse-proxy configuration.
- `justfile`: compile and run commands.

## Commands

Terminal 1:

```zsh
cd load-balancing
just server1
```

Terminal 2:

```zsh
cd load-balancing
just server2
```

Terminal 3:

```zsh
cd load-balancing
just nginx
```

Terminal 4:

```zsh
cd load-balancing
just client
just client-count 20
```

The client output shows which backend answered each request. The server terminals show how Nginx distributes traffic between the two backend processes.
