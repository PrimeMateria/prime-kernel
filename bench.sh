#!/usr/bin/env bash
set -euo pipefail

# PRIME Kernel Lean - Performance Benchmark Launcher
# Runs multi-tier benchmark batteries and records performance reports

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RUSTUP_TOOLCHAIN="1.97.1-x86_64-unknown-linux-gnu"
export PATH="${HOME}/.local/bin:${HOME}/.cargo/bin:${HOME}/.elan/bin:${PATH}"

cd "${SCRIPT_DIR}"
exec python3 "${SCRIPT_DIR}/benchmarks/run_benchmarks.py" "$@"
