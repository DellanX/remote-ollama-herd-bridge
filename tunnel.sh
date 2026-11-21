#!/usr/bin/env bash
set -euo pipefail

if [ -z "${VASTAI_HOST:-}" ]; then
    echo "VASTAI_HOST not set"
    exit 1
fi

if [ -z "${VASTAI_PORT:-}" ]; then
    echo "VASTAI_PORT not set"
    exit 1
fi

echo "Opening tunnel to ${VASTAI_HOST}:${VASTAI_PORT}"

exec ssh \
    -o StrictHostKeyChecking=no \
    -o UserKnownHostsFile=/dev/null \
    -N \
    -L 0.0.0.0:11434:localhost:11434 \
    -p "${VASTAI_PORT}" \
    root@"${VASTAI_HOST}"