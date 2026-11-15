#!/bin/bash
set -e

echo "Starting Ollama..."
ollama serve &

sleep 10

if [ -n "$HERD_ROUTER_URL" ]; then
    echo "Using explicit router: $HERD_ROUTER_URL"
    exec herd-node --router-url "$HERD_ROUTER_URL"
else
    echo "No HERD_ROUTER_URL specified, using mDNS discovery"
    exec herd-node
fi