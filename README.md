# Vast Herd Node

A lightweight Docker image that combines **Ollama** and **Ollama Herd Node**, making it easy to add GPUs to an existing Ollama Herd cluster.

This image was originally created for use with Vast.ai default jobs, but can run anywhere Docker is available.

## Features

- Runs Ollama with GPU acceleration
- Starts an Ollama Herd node automatically
- Supports explicit router configuration via environment variable
- Falls back to automatic mDNS router discovery when no router URL is provided
- Minimal configuration required
- Suitable for Vast.ai default jobs, homelabs, and dedicated inference nodes

## Quick Start

### Connect to a specific Herd router

```bash
docker run --rm \
  --gpus all \
  -e HERD_ROUTER_URL=http://192.168.0.79:11435 \
  ghcr.io/dellanx/vast-herd-node:latest
```

### Use automatic mDNS discovery

```bash
docker run --rm \
  --gpus all \
  ghcr.io/dellanx/vast-herd-node:latest
```

## Environment Variables

| Variable | Description | Default |
|-----------|------------|---------|
| `HERD_ROUTER_URL` | Explicit Ollama Herd router URL | mDNS discovery |
| `OLLAMA_HOST` | Address Ollama binds to | `0.0.0.0:11434` |

## How It Works

1. Starts the local Ollama service.
2. Waits for Ollama to become available.
3. Starts `herd-node`.
4. Connects to the configured router or discovers one via mDNS.
5. Makes the local GPU available to the Herd cluster.

## Vast.ai Default Job Example

This image is particularly useful as a Vast.ai default job:

- GPU sits idle
- Default job starts automatically
- Node joins Herd cluster
- Inference workloads are routed to the GPU
- Default job is paused automatically when a customer rents the machine
- Default job resumes when the GPU becomes idle again

## Logs

The container prints startup diagnostics including:

- Ollama startup status
- Herd node startup status
- Router connectivity checks
- Network information useful for troubleshooting

## Security

This image contains no built-in VPN configuration, credentials, or authentication material.

If your Herd router is not publicly reachable, use a secure networking solution such as:

- Tailscale
- WireGuard
- Site-to-site VPN
- Private networking infrastructure

Credentials should be injected at deployment time and not baked into the image.

## License

This project is provided as-is and relies on the upstream Ollama and Ollama Herd projects.