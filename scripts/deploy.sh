#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl is not installed." >&2
  exit 1
fi

if ! kubectl config current-context >/dev/null 2>&1; then
  echo "No active Kubernetes context. Start a cluster and configure kubectl first." >&2
  exit 1
fi

if ! kubectl cluster-info >/dev/null 2>&1; then
  echo "Kubernetes API server is unreachable for the current context." >&2
  echo "If you are using Docker Desktop, minikube, kind, or Rancher Desktop, start that cluster first." >&2
  exit 1
fi

kubectl apply -f "$ROOT_DIR/infrastructure/kubernetes/namespace.yaml"
kubectl apply -k "$ROOT_DIR/infrastructure/kubernetes"
