#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT_DIR"

python3 -m grpc_tools.protoc \
  -I=proto \
  --python_out=. \
  --grpc_python_out=. \
  proto/log.proto
