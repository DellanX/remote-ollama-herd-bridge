# Vast Ollama Herd

A lightweight pair of Docker images for building distributed Ollama clusters across Vast.ai and local infrastructure using Ollama Herd.

This project publishes two images:

| Image | Purpose |
|---------|---------|
| `ghcr.io/dellanx/vast-herd-node` | GPU-powered Ollama node deployed on Vast.ai |
| `ghcr.io/dellanx/vast-herd-router` | Local Herd router that discovers Vast.ai instances and connects them through SSH tunnels |

---

## Architecture

```text
+-------------------+
| Local Network     |
|                   |
| Router Container  |
| herd-node         |
+---------+---------+
          |
          | SSH Tunnel
          |
+---------v---------+
| Vast.ai Instance  |
|                   |
| Ollama            |
| GPU Models        |
+-------------------+
```

The router image automatically:

1. Discovers Vast.ai instances.
2. Selects an instance by ID, label, or automatic discovery.
3. Establishes an SSH tunnel to the remote node.
4. Exposes the remote Ollama API locally.
5. Starts `herd-node`.
6. Optionally notifies a webhook once online.

---

# Node Image

Image:

```text
ghcr.io/dellanx/vast-herd-node
```

The Node image provides:

- Ollama
- NVIDIA GPU support
- Vast.ai compatibility
- Native Ollama logging
- SSH accessibility through Vast.ai

---

## Run Locally

```bash
docker run \
  --rm \
  --gpus all \
  -p 11434:11434 \
  ghcr.io/dellanx/vast-herd-node:latest
```

Ollama becomes available at:

```text
http://localhost:11434
```

---

## Pull Models

```bash
docker exec -it <container> ollama pull llama3.2
```

---

## Query Models

```bash
curl http://localhost:11434/api/tags
```

---

## Vast.ai Default Job

Example:

```bash
vastai set defjob <machine-id> \
  --image ghcr.io/dellanx/vast-herd-node:latest \
  --price_gpu 0.01
```

Workflow:

1. Machine becomes idle.
2. Vast.ai launches the job.
3. Ollama starts.
4. GPU becomes available for inference.
5. Router containers discover the node automatically.
6. Job pauses when rented.

---

# Router Image

Image:

```text
ghcr.io/dellanx/vast-herd-router
```

The Router image manages connectivity between Herd and Vast.ai.

Built-in components:

- vastai CLI
- herd-node
- SSH client
- jq
- discovery scripts
- tunnel management
- webhook notifications

---

## Router Startup Flow

```text
identify
    ↓
tunnel
    ↓
wait-for-tunnel
    ↓
start-herd
    ↓
notify-online
```

Each stage can be skipped by pre-populating its required state.

This makes local development and debugging significantly easier.

---

## Example Router Deployment

```bash
docker run \
  --restart unless-stopped \
  -e VASTAI_API_KEY=xxxxxxxx \
  -e ROUTER_URL=https://router.example.com \
  -e NODE_ID=router-01 \
  ghcr.io/dellanx/vast-herd-router:latest
```

---

## Discovery Modes

### Explicit Instance

```bash
-e VASTAI_INSTANCE_ID=12345678
```

Router will connect directly to that instance.

---

### Label-Based Discovery

```bash
-e VASTAI_INSTANCE_LABEL=router
```

Router selects the first running instance matching the label.

If multiple instances match:

```text
router
router
router
```

the lowest-id running instance is selected.

---

### Automatic Discovery

```bash
-e VASTAI_API_KEY=xxxxxxxx
```

Router automatically selects the first running instance.

---

## Development Overrides

Discovery can be skipped entirely.

Example:

```bash
docker run \
  -e VASTAI_HOST=1.2.3.4 \
  -e VASTAI_PORT=40222 \
  ghcr.io/dellanx/vast-herd-router:latest
```

No Vast.ai API calls are made.

This is useful for:

- Local testing
- SSH validation
- Tunnel debugging

---

## Webhook Notifications

Optional:

```bash
-e ONLINE_WEBHOOK=https://example.com/webhook
```

Payload:

```json
{
  "status": "online",
  "node_id": "router-01",
  "instance_id": 12345678,
  "host": "1.2.3.4",
  "port": 40222
}
```

Webhook failures are ignored and do not stop startup.

---

## Environment Variables

### Node Image

| Variable | Description | Default |
|-----------|-------------|---------|
| `OLLAMA_HOST` | Ollama bind address | `0.0.0.0:11434` |

---

### Router Image

| Variable | Description |
|-----------|-------------|
| `VASTAI_API_KEY` | Vast.ai API key |
| `VASTAI_INSTANCE_ID` | Direct instance selection |
| `VASTAI_INSTANCE_LABEL` | Label-based selection |
| `VASTAI_INSTANCE_INDEX` | Match index for duplicate labels |
| `VASTAI_HOST` | Manual host override |
| `VASTAI_PORT` | Manual port override |
| `ROUTER_URL` | Herd router URL |
| `NODE_ID` | Herd node ID |
| `ONLINE_WEBHOOK` | Optional startup webhook |
| `WAIT_MAX_RETRIES` | Tunnel startup retry limit |
| `WAIT_INTERVAL` | Seconds between retries |

---

## Security

This project contains:

- No embedded API keys
- No embedded SSH keys
- No VPN configuration
- No authentication tokens
- No default credentials

All access control should be managed externally.

Recommended approaches:

- SSH tunnels
- Tailscale
- WireGuard
- Reverse proxies
- Private networking

---

## Use Cases

### Vast.ai Default Jobs

Automatically host Ollama on idle cloud GPUs.

### Distributed Ollama Herd

Combine local and cloud-hosted nodes into a single cluster.

### Hybrid AI Infrastructure

Burst inference workloads into Vast.ai while maintaining local routing.

### Homelab GPU Expansion

Attach temporary cloud GPUs to an existing Herd deployment.

---

## License

This project is provided as-is and depends on upstream projects including:

- Ollama
- Ollama Herd
- Vast.ai

Refer to their respective licenses and documentation for details.