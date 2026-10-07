#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"

if ! command -v dot >/dev/null 2>&1; then
    echo "Graphviz is required. Install the 'graphviz' system package first." >&2
    exit 1
fi

python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -r "${PROJECT_DIR}/requirements.txt"

echo "Installation completed. Run: ${VENV_DIR}/bin/python ${PROJECT_DIR}/main.py"
