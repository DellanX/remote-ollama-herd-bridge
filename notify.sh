#!/usr/bin/env bash
set -euo pipefail

if [ -z "${ONLINE_WEBHOOK:-}" ]; then
    exit 0
fi

curl \
    -fsS \
    -X POST \
    -H 'Content-Type: application/json' \
    --data "$(
        jq -n \
            --arg node "${NODE_ID:-unknown}" \
            --arg instance "${VASTAI_INSTANCE_ID_SELECTED:-unknown}" \
            --arg host "${VASTAI_HOST:-unknown}" \
            --arg port "${VASTAI_PORT:-unknown}" '
            {
                status:"online",
                node_id:$node,
                instance_id:$instance,
                host:$host,
                port:$port
            }
        '
    )" \
    "${ONLINE_WEBHOOK}" \
    || true