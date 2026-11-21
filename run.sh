#!/usr/bin/env bash
set -euo pipefail

#
# Resolve instance
#

if [ -z "${VASTAI_HOST:-}" ] || \
   [ -z "${VASTAI_PORT:-}" ]; then

    INSTANCE_JSON="$(identify --json)"

    export VASTAI_INSTANCE_ID_SELECTED="$(
        jq -r '.id' <<< "$INSTANCE_JSON"
    )"

    export VASTAI_HOST="$(
        jq -r '.host' <<< "$INSTANCE_JSON"
    )"

    export VASTAI_PORT="$(
        jq -r '.port' <<< "$INSTANCE_JSON"
    )"
fi

#
# Resolve tunnel
#

if [ -z "${SSH_PID:-}" ]; then

    tunnel &
    export SSH_PID=$!

fi

#
# Synchronize
#

wait-for-tunnel "${SSH_PID}"

#
# Resolve herd
#

if [ -z "${HERD_PID:-}" ]; then

    start-herd &
    export HERD_PID=$!

fi

#
# Notify
#

notify-online || true

#
# Container lifetime
#

wait "${HERD_PID}"