#!/usr/bin/env bash
set -euo pipefail

echo "Installing VastAI CLI..."

python3 -m pip install --upgrade pip

pip3 install \
    vastai \
    herd-node

export PATH="/root/.local/bin:$PATH"

echo "Installed versions"

vastai --version || true
herd-node --help >/dev/null || true