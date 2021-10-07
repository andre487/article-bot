#!/usr/bin/env bash
set -eufo pipefail
cd "$(dirname "$0")"

echo '===> Create venv'
python3 -m venv .venv

echo '===> Update pip'
.venv/bin/python -m pip install -U pip

echo '===> Install requirements'
.venv/bin/python -m pip install -r requirements.txt
