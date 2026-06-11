#!/usr/bin/env bash
set -euo pipefail
uvicorn backend.api.main:app --reload

