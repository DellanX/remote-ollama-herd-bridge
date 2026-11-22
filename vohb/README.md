# VOHB

**Virtual Ollama Herd Bridge**

VOHB is a lightweight bridge between **Vast.ai** and **Ollama Herd**.

It discovers Vast.ai instances, establishes secure SSH tunnels to remote Ollama nodes, waits for connectivity, and then launches `herd-node` using the tunneled endpoint.

The goal is to allow cloud-hosted Ollama instances to participate in a local Ollama Herd deployment without requiring direct network exposure.

---

## Features

- Vast.ai instance discovery
- Instance selection by ID
- Instance selection by label
- Automatic discovery of running instances
- SSH tunnel management
- Readiness checks
- Ollama Herd integration
- Environment variable support
- CLI argument overrides
- Local development friendly

---

## Installation

### Using uv

```bash
uv add vohb
```

### Development

```bash
git clone <repository>
cd vohb

uv sync
```

Run the CLI:

```bash
uv run vohb run
```

---

## Concepts

VOHB manages three stages:

```text
identify
    ↓
tunnel
    ↓
herd-node
```

### Identify

Resolve a target Vast.ai instance.

Sources are checked in the following order:

```text
1. Manual host/port
2. Instance ID
3. Instance label
4. First running instance
```

### Tunnel

Create an SSH tunnel from a local port to the remote Ollama instance.

Example:

```text
localhost:11434
    ↓
vast.ai instance
    ↓
localhost:11434
```

### Herd

Launches `herd-node` using the local side of the tunnel.

---

## Commands

### Run

Default Command:

```bash
vohb run
```

Startup flow:

```text
identify
    ↓
tunnel
    ↓
wait
    ↓
herd-node
```

---

### Identify

Discover the target instance.

```bash
vohb identify
```

Example output:

```json
{
  "id": 123456,
  "host": "1.2.3.4",
  "port": 40222,
  "label": "router",
  "status": "running"
}
```

---

### Tunnel

Create and validate an SSH tunnel.

```bash
vohb tunnel
```

Or manually specify a target:

```bash
vohb tunnel \
  --host 1.2.3.4 \
  --port 40222
```

---

### Herd

Launch Herd directly.

```bash
vohb herd
```

Useful for testing an existing tunnel.

---

## Configuration

### Vast.ai Discovery

| Variable | Description |
|-----------|-------------|
| `VASTAI_API_KEY` | Vast.ai API key |
| `VASTAI_INSTANCE_ID` | Direct instance selection |
| `VASTAI_INSTANCE_LABEL` | Instance label |
| `VASTAI_INSTANCE_INDEX` | Index within matching labels |
| `VASTAI_HOST` | Manual host override |
| `VASTAI_PORT` | Manual port override |

---

### Tunnel

| Variable | Description |
|-----------|-------------|
| `SSH_USER` | SSH username |
| `SSH_IDENTITY_FILE` | SSH private key path |
| `LOCAL_HOST` | Local bind address |
| `LOCAL_PORT` | Local bind port |
| `REMOTE_HOST` | Remote host |
| `REMOTE_PORT` | Remote port |
| `WAIT_INTERVAL` | Seconds between readiness checks |
| `WAIT_MAX_RETRIES` | Maximum readiness attempts |

---

### Herd

| Variable | Description |
|-----------|-------------|
| `NODE_ID` | Herd node identifier |
| `ROUTER_URL` | Herd router URL |
| `LEARN_CAPACITY` | Enable adaptive capacity learning |
| `LOG_LEVEL` | Logging level |

---

## Examples

### Connect to a Specific Vast.ai Instance

```bash
vohb run \
  --instance-id 12345678
```

### Connect by Label

```bash
vohb run \
  --instance-label inference
```

### Skip Discovery Completely

```bash
vohb run \
  --host 1.2.3.4 \
  --port 40222
```

### Use a Specific SSH Identity

```bash
vohb run \
  --ssh-identity-file ~/.ssh/id_ed25519
```

### Custom Tunnel Port

```bash
vohb run \
  --local-port 11435
```

---

## Architecture

```text
+-------------+
| Ollama Herd |
| Router      |
+------+------+
       ^
       |
       |
+------+------+
| VOHB         |
| SSH Tunnel   |
+------+------+
       |
       |
       v
+------+------+
| Vast.ai      |
| Ollama Node  |
+-------------+
```

---

## Security

VOHB does not store credentials.

Recommended authentication:

```text
SSH public/private keys
```

Avoid password-based authentication whenever possible.

---

## License

MIT