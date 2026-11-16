#!/bin/bash
set -e

ROUTER_URL=""
NODE_ID=""

#
# Parse CLI arguments
#
while [[ $# -gt 0 ]]; do
    case "$1" in
        --router-url)
            ROUTER_URL="$2"
            shift 2
            ;;
        --node-id)
            NODE_ID="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            shift
            ;;
    esac
done

#
# Environment variable fallbacks
#
ROUTER_URL="${ROUTER_URL:-${HERD_ROUTER_URL:-}}"
NODE_ID="${NODE_ID:-${HERD_NODE_ID:-$(hostname)}}"

echo "========================================"
echo "Vast Herd Node Startup"
echo "========================================"
echo "Node ID: $NODE_ID"
echo "Router URL: ${ROUTER_URL:-mDNS discovery}"
echo "Tailscale: ${TS_AUTHKEY:+enabled}"
echo "========================================"

#
# Optional Tailscale startup
#
if [ -n "${TS_AUTHKEY:-}" ]; then
    echo "Starting Tailscale..."

    tailscaled \
    --tun=userspace-networking \
    --socks5-server=localhost:1055 \
    --outbound-http-proxy-listen=localhost:1055 \
    --state=/tmp/tailscaled.state &
    TAILSCALED_PID=$!

    sleep 10

    TS_ARGS=( "--authkey=${TS_AUTHKEY}" )

    if [ -n "$NODE_ID" ]; then
        TS_ARGS+=( "--hostname=${NODE_ID}" )
    fi

    tailscale up "${TS_ARGS[@]}"

    echo "Tailscale status:"
    tailscale status || true

    echo "Tailscale IPs:"
    tailscale ip || true
fi

#
# Start Ollama
#
echo "Starting Ollama..."

export OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"

ollama serve &
OLLAMA_PID=$!

echo "Waiting for Ollama to initialize..."
sleep 10

#
# Connectivity diagnostics
#
if [ -n "$ROUTER_URL" ]; then
    echo "Testing Herd router connectivity..."
    curl -v "$ROUTER_URL" || true
fi

#
# Start Herd Node
#
echo "Starting Herd Node..."

if [ -n "$ROUTER_URL" ]; then
    echo "Using configured router: $ROUTER_URL"

    exec herd-node \
        --router-url "$ROUTER_URL"
else
    echo "No router URL specified, using mDNS discovery"

    exec herd-node
fi
