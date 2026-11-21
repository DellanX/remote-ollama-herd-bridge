#!/usr/bin/env bash
set -euo pipefail

export PATH="/root/.local/bin:$PATH"

OUTPUT="env"

if [ "${1:-}" = "--json" ]; then
    OUTPUT="json"
fi

########################################
# API Key
########################################

if [ -z "${VASTAI_API_KEY:-}" ]; then
    echo "ERROR: VASTAI_API_KEY not set" >&2
    exit 1
fi

export VAST_API_KEY="$VASTAI_API_KEY"

########################################
# Discovery Mode
########################################

MODE="auto"

if [ -n "${VASTAI_INSTANCE_ID:-}" ]; then
    MODE="id"
elif [ -n "${VASTAI_INSTANCE_LABEL:-}" ]; then
    MODE="label"
fi

########################################
# Instance Selection
########################################

case "$MODE" in
    id)

        INSTANCE_JSON="$(
            vastai show instance \
                "${VASTAI_INSTANCE_ID}" \
                --raw
        )"

        ;;

    label)

        IDX="${VASTAI_INSTANCE_INDEX:-0}"

        INSTANCE_JSON="$(
            vastai show instances --raw |
            jq -c \
                --arg label "${VASTAI_INSTANCE_LABEL}" \
                --argjson idx "${IDX}" '
                    map(
                        select(
                            .label == $label and
                            .actual_status == "running"
                        )
                    )
                    | sort_by(.id)
                    | .[$idx]
                '
        )"

        ;;

    auto)

        INSTANCE_JSON="$(
            vastai show instances --raw |
            jq -c '
                map(
                    select(
                        .actual_status == "running"
                    )
                )
                | sort_by(.id)
                | .[0]
            '
        )"

        ;;

esac

########################################
# Validation
########################################

if [ -z "${INSTANCE_JSON}" ] || [ "${INSTANCE_JSON}" = "null" ]; then
    echo "ERROR: No matching instance found" >&2
    exit 1
fi

########################################
# Build Output Object
########################################

RESULT="$(
    echo "${INSTANCE_JSON}" |
    jq -c '
    {
        id: .id,
        label: (.label // ""),
        status: .actual_status,

        host: (
            .public_ipaddr
            // .ssh_host
            // .host
        ),

        port: (
            .ssh_port
            // .ports["22/tcp"][0].HostPort
        )
    }'
)"

########################################
# JSON Mode
########################################

if [ "${OUTPUT}" = "json" ]; then
    echo "${RESULT}"
    exit 0
fi

########################################
# ENV Mode
########################################

INSTANCE_ID="$(
    echo "$RESULT" | jq -r '.id'
)"

HOST="$(
    echo "$RESULT" | jq -r '.host'
)"

PORT="$(
    echo "$RESULT" | jq -r '.port'
)"

cat > /tmp/vastai.env <<EOF
export VASTAI_INSTANCE_ID_SELECTED=${INSTANCE_ID}
export VASTAI_HOST=${HOST}
export VASTAI_PORT=${PORT}
EOF

echo "Selected instance ${INSTANCE_ID}"
echo "Host: ${HOST}"
echo "Port: ${PORT}"
echo "Environment saved to /tmp/vastai.env"