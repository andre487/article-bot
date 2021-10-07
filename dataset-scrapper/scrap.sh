#!/usr/bin/env bash
set -eufo pipefail
cd "$(dirname "$0")"

.venv/bin/python main.py "$@"
