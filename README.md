# Vast Herd Node

A lightweight Docker image that combines **Ollama** and **Ollama Herd Node** to easily add local or cloud GPUs to an existing Ollama Herd cluster.

Originally created for **Vast.ai Default Jobs**, this image can run anywhere Docker and GPU acceleration are available.

---

## Features

- GPU-accelerated Ollama server
- Automatic Ollama Herd node startup
- Explicit router configuration via CLI arguments
- Environment variable configuration support
- Automatic mDNS router discovery fallback
- Startup diagnostics and connectivity testing
- Designed for Vast.ai Default Jobs, homelabs, and dedicated inference nodes

---

## Quick Start

### Connect to a Specific Router (CLI Argument)

```bash
docker run --rm \
  --gpus all \
  ghcr.io/dellanx/vast-herd-node:latest \
  --router-url http://192.168.0.79:11435
```

### Connect to a Specific Router (Environment Variable)

```bash
docker run --rm \
  --gpus all \
  -e HERD_ROUTER_URL=http://192.168.0.79:11435 \
  ghcr.io/dellanx/vast-herd-node:latest
```

### Use Automatic mDNS Discovery

```bash
docker run --rm \
  --gpus all \
  ghcr.io/dellanx/vast-herd-node:latest
```

When no router URL is specified, the container falls back to Ollama Herd's built-in mDNS discovery mechanism.

---

## Vast.ai Default Job Example

A common use case is automatically contributing idle GPUs to an Ollama Herd cluster.

Example:

```bash
vastai set defjob <machine-id> \
  --image ghcr.io/dellanx/vast-herd-node:latest \
  --price_gpu 0.01 \
  --args "--router-url http://192.168.0.79:11435"
```

Workflow:

1. GPU becomes idle.
2. Vast.ai launches the default job.
3. Ollama starts.
4. Herd Node joins the cluster.
5. Inference requests are routed to the idle GPU.
6. The job is paused automatically when a customer rents the machine.
7. The job resumes when the machine becomes idle again.

---

## Supported Configuration

### CLI Arguments

| Argument | Description |
|-----------|------------|
| `--router-url` | Explicit Herd router address |

Example:

```bash
docker run ghcr.io/dellanx/vast-herd-node:latest \
  --router-url http://192.168.0.79:11435
```

### Environment Variables

| Variable | Description | Default |
|-----------|------------|---------|
| `HERD_ROUTER_URL` | Explicit Herd router URL | mDNS discovery |
| `OLLAMA_HOST` | Address Ollama binds to | `0.0.0.0:11434` |

CLI arguments take precedence over environment variables.

---

## How It Works

At startup the container:

1. Starts the local Ollama service.
2. Performs basic startup diagnostics.
3. Waits for Ollama to become available.
4. Determines the router URL from:
   - `--router-url`
   - `HERD_ROUTER_URL`
   - mDNS discovery
5. Launches `herd-node`.
6. Registers with the Herd router.
7. Makes local GPU resources available to the cluster.

---

## Diagnostics

Startup logs include information that can help troubleshoot networking and cluster registration:

- Ollama startup status
- Herd node startup status
- Router connectivity checks
- Environment configuration
- Network diagnostics

To view logs:

```bash
docker logs <container>
```

---

## Security

This image contains:

- No VPN configuration
- No embedded credentials
- No authentication tokens
- No network secrets

Any networking or authentication requirements should be provided at deployment time.

Common deployment approaches include:

- Tailscale
- WireGuard
- Site-to-site VPNs
- Private cloud networking

Never bake sensitive credentials into a public container image.

---

## Use Cases

### Vast.ai Default Jobs

Automatically contribute idle GPUs to a Herd cluster.

### Homelab GPU Pooling

Aggregate multiple desktop, server, and laptop GPUs into a single Herd deployment.

### Dedicated Inference Workers

Run dedicated cloud inference workers that automatically join an existing Herd cluster.

### Hybrid Clusters

Combine local GPUs and cloud GPUs behind a single Herd router.

---

## Related Projects

- Ollama
- Ollama Herd
- Vast.ai

---

## License

This project is provided as-is and depends on the upstream Ollama and Ollama Herd projects.

Please refer to their respective licenses and documentation for details.