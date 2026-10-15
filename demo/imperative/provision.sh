#!/usr/bin/env bash
# DEMO 1 - the naive imperative script.
#
# Simulates provisioning a small web platform on a fake cloud
# (a local folder). Each command says HOW to do something, step by step.
#
# Run it twice and watch what happens:
#   ./provision.sh
#   ./provision.sh
set -e

CLOUD="${CLOUD_DIR:-.fakecloud-imperative}"

echo "Creating network..."
mkdir "$CLOUD"                                   # step 1: create the "VPC"

echo "Creating VMs..."
for vm in web-1 web-2; do
  echo "name=$vm size=small" > "$CLOUD/$vm.vm"   # step 2: create the VMs
done

echo "Registering VMs in the load balancer..."
for vm in web-1 web-2; do
  echo "$vm" >> "$CLOUD/load-balancer.pool"      # step 3: add to the pool
done

echo "Done."
