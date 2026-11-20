# Vast Ollama Node

A lightweight Docker image that combines the **Vast.ai Base Image** with **Ollama**, providing a GPU-accelerated inference node that can be deployed on Vast.ai, homelabs, or any Docker host with NVIDIA GPU support.

This image is designed to work seamlessly with **Vast.ai Default Jobs**, allowing idle GPUs to automatically host Ollama instances that can be connected through SSH tunnels, reverse proxies, VPNs, or other networking solutions.

---

## Features

- GPU-accelerated Ollama server
- Based on `vastai/base-image`
- Preserves Vast.ai SSH functionality
- Compatible with Vast.ai Default Jobs
- Minimal image footprint
- Runs Ollama as the primary container process
- Native Ollama logging and console output
- Works with local and cloud GPUs

---

## Quick Start

### Local Docker

```bash
docker run --rm \
  --gpus all \
  -p 11434:11434 \
  ghcr.io/dellanx/vast-ollama-node:latest
```

Ollama will be available at:

```text
http://localhost:11434
```

---

### Pull Models

```bash
docker exec -it <container> ollama pull llama3.2
```

---

### Query Ollama

```bash
curl http://localhost:11434/api/tags
```

---

## Vast.ai Default Job Example

A common use case is automatically exposing idle GPUs for inference workloads.

Example:

```bash
vastai set defjob <machine-id> \
  --image ghcr.io/dellanx/vast-ollama-node:latest \
  --price_gpu 0.01
```

Workflow:

1. GPU becomes idle.
2. Vast.ai launches the default job.
3. Ollama starts automatically.
4. The GPU becomes available for inference.
5. Customers can access the node through:
   - SSH tunnels
   - VPNs
   - Reverse proxies
   - Direct network exposure
6. The job is paused automatically when a customer rents the machine.
7. The job resumes when the machine becomes idle again.

---

## SSH Tunnel Example

A common deployment pattern is exposing the remote Ollama instance through an SSH tunnel.

Forward a local port:

```bash
ssh -N \
  -L 11434:localhost:11434 \
  root@<vast-instance>
```

You can then use the remote GPU exactly as if Ollama were running locally:

```bash
curl http://localhost:11434/api/tags
```

---

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|----------|
| `OLLAMA_HOST` | Listen address | `0.0.0.0:11434` |

Example:

```bash
docker run \
  --gpus all \
  -e OLLAMA_HOST=0.0.0.0:11434 \
  ghcr.io/dellanx/vast-ollama-node:latest
```

---

## How It Works

At startup the container:

1. Initializes the Vast.ai base environment.
2. Starts Ollama.
3. Detects available NVIDIA GPUs.
4. Exposes the Ollama API on port 11434.
5. Writes standard Ollama logs to the container console.

Because Ollama runs as the foreground process, logs behave exactly as they do in the official `ollama/ollama` image.

---

## Diagnostics

View logs:

```bash
docker logs <container>
```

Example output:

```text
time=2026-11-19T12:00:00Z level=INFO msg="server config"
time=2026-11-19T12:00:01Z level=INFO msg="looking for compatible GPUs"
time=2026-11-19T12:00:02Z level=INFO msg="listening on [::]:11434"
```

---

## Security

This image contains:

- No embedded credentials
- No authentication tokens
- No VPN software
- No network configuration
- No SSH keys

Networking and access control should be managed externally.

Common approaches include:

- SSH tunnels
- Tailscale
- WireGuard
- Reverse proxies
- Private cloud networking

Never bake credentials into a public container image.

---

## Use Cases

### Vast.ai Default Jobs

Automatically host Ollama on idle rented GPUs.

### Remote GPU Inference

Run Ollama on cloud GPUs while keeping clients local.

### Homelab GPU Hosting

Make spare desktop or server GPUs available through Ollama.

### Hybrid AI Infrastructure

Combine local and cloud-hosted Ollama instances behind a shared routing layer.

---

## Related Projects

- Ollama
- Vast.ai

---

## License

This project is provided as-is and depends on the upstream Ollama and Vast.ai projects.

Please refer to their respective licenses and documentation for details.