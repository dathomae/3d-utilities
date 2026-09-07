#!/usr/bin/env bash
set -euo pipefail

# Thin wrapper that bootstraps the worktree environment from the repo root.
cd "$(dirname "$0")/.."

if [[ ! -d .venv ]]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip -q
.venv/bin/python -m pip install -e . -q
