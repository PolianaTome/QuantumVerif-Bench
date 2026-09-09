#!/usr/bin/env bash
# Runs ESBMC on the QuantumVerif-Bench benchmarks and saves each verification
# log under results/<benchmark-name>.log.
#
# Usage:
#   scripts/run_esbmc.sh                       # run all benchmarks/*/*.py (except _spike)
#   scripts/run_esbmc.sh benchmarks/bell/bell.py [more files...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

mkdir -p "$PROJECT_ROOT/results"

run_one() {
    local file="$1"
    local name
    name="$(basename "$(dirname "$file")")"
    local log="$PROJECT_ROOT/results/${name}.log"

    echo "==> Verifying $file"
    if esbmc --python "$PYTHON_BIN" "$file" > "$log" 2>&1; then
        echo "    VERIFICATION SUCCESSFUL -> $log"
    else
        echo "    VERIFICATION FAILED or ERROR -> $log"
    fi
}

if [ "$#" -ge 1 ]; then
    for file in "$@"; do
        run_one "$file"
    done
else
    for file in "$PROJECT_ROOT"/benchmarks/*/*.py; do
        dir_name="$(basename "$(dirname "$file")")"
        if [ "$dir_name" = "_spike" ]; then
            continue
        fi
        run_one "$file"
    done
fi
