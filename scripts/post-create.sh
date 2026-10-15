#!/usr/bin/env bash
# Runs once when the codespace is created. Installs the tools that are not
# available as dev container features. Safe to re-run (idempotent).
set -euo pipefail

echo "==> Installing Ansible (user scope, via pipx)"
if ! command -v ansible >/dev/null 2>&1; then
  python3 -m pip install --user --quiet pipx
  python3 -m pipx ensurepath >/dev/null
  python3 -m pipx install --include-deps ansible >/dev/null
else
  echo "    already installed, skipping"
fi

echo "==> Installing kind (Kubernetes in Docker)"
KIND_VERSION="v0.27.0"
if ! command -v kind >/dev/null 2>&1; then
  curl -fsSLo /tmp/kind "https://kind.sigs.k8s.io/dl/${KIND_VERSION}/kind-linux-amd64"
  sudo install -m 0755 /tmp/kind /usr/local/bin/kind
  rm -f /tmp/kind
else
  echo "    already installed, skipping"
fi

echo "==> Making course scripts executable"
chmod +x scripts/*.sh demo/imperative/*.sh

echo
echo "Toolbox ready. Run:  make check"
