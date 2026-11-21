#!/usr/bin/env bash
set -euo pipefail

SSH_PID="${1:?missing ssh pid}"

INTERVAL="${WAIT_INTERVAL:-1}"
MAX_RETRIES="${WAIT_MAX_RETRIES:-10}"

ATTEMPT=0

echo "Waiting for tunnel process ${SSH_PID}"

while true
do
    if ! kill -0 "${SSH_PID}" 2>/dev/null; then
        echo "Tunnel process exited"
        exit 1
    fi

    ATTEMPT=$((ATTEMPT + 1))

    if [ "${ATTEMPT}" -ge "${MAX_RETRIES}" ]; then
        echo "Tunnel considered established"
        exit 0
    fi

    sleep "${INTERVAL}"
done