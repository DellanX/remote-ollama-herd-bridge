#!/usr/bin/env bash
set -euo pipefail

ARGS=()

if [ -n "${ROUTER_URL:-}" ]; then
    ARGS+=(--router-url "${ROUTER_URL}")
fi

if [ -n "${NODE_ID:-}" ]; then
    ARGS+=(--node-id "${NODE_ID}")
fi

if [ -n "${HERD_NODE_ARGS:-}" ]; then
    read -ra EXTRA <<< "${HERD_NODE_ARGS}"
    ARGS+=("${EXTRA[@]}")
fi

echo "Launching herd-node"

exec herd-node "${ARGS[@]}"