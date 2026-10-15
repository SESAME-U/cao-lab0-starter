#!/usr/bin/env bash
# DEMO 2 - the same script, made idempotent by hand.
#
# Every step now checks the current state before acting:
# "create only if missing", "add only if absent".
# Run it as many times as you like: the result is the same.
#
# Notice the cost: each step needs its own guard, and the script still
# cannot REMOVE something you took out of the list. That is the job of a
# declarative tool (see ../declarative).
set -e

CLOUD="${CLOUD_DIR:-.fakecloud-imperative}"
VMS=(web-1 web-2)

echo "Ensuring network..."
mkdir -p "$CLOUD"

echo "Ensuring VMs..."
for vm in "${VMS[@]}"; do
  desired="name=$vm size=small"
  if [[ ! -f "$CLOUD/$vm.vm" ]] || [[ "$(cat "$CLOUD/$vm.vm")" != "$desired" ]]; then
    echo "$desired" > "$CLOUD/$vm.vm"
    echo "  $vm: created or corrected"
  else
    echo "  $vm: already correct"
  fi
done

echo "Ensuring load balancer pool..."
touch "$CLOUD/load-balancer.pool"
for vm in "${VMS[@]}"; do
  if ! grep -qx "$vm" "$CLOUD/load-balancer.pool"; then
    echo "$vm" >> "$CLOUD/load-balancer.pool"
    echo "  $vm: added"
  else
    echo "  $vm: already registered"
  fi
done

echo "Done."
