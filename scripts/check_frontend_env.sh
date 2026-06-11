#!/usr/bin/env bash
set -euo pipefail

if ! command -v node >/dev/null 2>&1; then
  cat <<'EOF'
Node.js was not found in this Linux environment.

This usually happens on WSL 1 when only Windows Node/npm is installed.
Use one of these supported options:

1. Upgrade the distro to WSL 2, then install Linux Node.js 20+.
2. Run the frontend from Windows PowerShell:
   cd path\to\Compiler_pbl\frontend
   npm install
   npm run dev
3. Use Docker:
   docker compose up --build frontend

The exposed /mnt/c Windows npm shim cannot reliably run inside WSL 1.
EOF
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm was not found. Install Node.js 20+ with npm, then retry."
  exit 1
fi

echo "Node: $(node --version)"
echo "npm: $(npm --version)"
echo "Frontend environment looks ready."

