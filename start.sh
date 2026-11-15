#!/bin/bash
set -e

ROUTER_URL=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --router-url)
            ROUTER_URL="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            shift
            ;;
    esac
done

# Env var fallback
if [ -z "$ROUTER_URL" ]; then
    ROUTER_URL="${HERD_ROUTER_URL:-}"
fi

echo "Starting Ollama..."
export OLLAMA_HOST="${OLLAMA_HOST:-0.0.0.0:11434}"
ollama serve &

sleep 10

if [ -n "$ROUTER_URL" ]; then
    echo "Using Herd router: $ROUTER_URL"

    echo "Testing connectivity..."
    curl -v "$ROUTER_URL" || true

    exec herd-node --router-url "$ROUTER_URL"
else
    echo "No router URL specified, using mDNS discovery"
    exec herd-node
fi