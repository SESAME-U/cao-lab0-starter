#!/usr/bin/env python3
"""DEMO 3 - a tiny declarative engine (desired state + reconciliation).

You describe WHAT you want in desired.json. The engine reads the ACTUAL
state of the fake cloud, computes the difference (the plan), and applies
only the changes needed to make actual == desired.

This is, in miniature, what Terraform, Kubernetes controllers and
Argo CD all do.

Usage:
    python3 reconcile.py plan     # show what would change, change nothing
    python3 reconcile.py apply    # converge the fake cloud to desired.json
    python3 reconcile.py show     # print the actual state

The fake cloud is a folder (default: .fakecloud) with one JSON file per
resource. Edit those files by hand to simulate drift.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESIRED_FILE = Path(os.environ.get("DESIRED_FILE", HERE / "desired.json"))
CLOUD_DIR = Path(os.environ.get("CLOUD_DIR", HERE / ".fakecloud"))


@dataclass(frozen=True)
class Change:
    action: str          # "create" | "update" | "delete"
    name: str
    before: dict | None
    after: dict | None


# ---------------------------------------------------------------- state I/O

def load_desired(path: Path = DESIRED_FILE) -> dict[str, dict]:
    """Return {name: resource} from the desired-state file."""
    data = json.loads(path.read_text())
    resources = {}
    for res in data["resources"]:
        if res["name"] in resources:
            raise ValueError(f"duplicate resource name: {res['name']}")
        resources[res["name"]] = res
    return resources


def load_actual(cloud: Path = CLOUD_DIR) -> dict[str, dict]:
    """Return {name: resource} from what currently exists in the fake cloud."""
    if not cloud.exists():
        return {}
    return {p.stem: json.loads(p.read_text()) for p in sorted(cloud.glob("*.json"))}


# ------------------------------------------------------------------- the diff

def compute_plan(desired: dict[str, dict], actual: dict[str, dict]) -> list[Change]:
    """Compare desired and actual state and return the list of changes.

    - in desired, not in actual            -> create
    - in both, but different               -> update
    - in actual, not in desired            -> delete
    - in both and identical                -> nothing (no-op)
    """
    plan: list[Change] = []

    for name, want in desired.items():
        have = actual.get(name)
        if have is None:
            plan.append(Change("create", name, None, want))
        elif have != want:
            plan.append(Change("update", name, have, want))

    # TODO (Lab 0, exercise C): detect resources that exist in the cloud
    # but are no longer in desired.json, and add a "delete" Change for each.
    # Hint: loop over `actual`, and look at how "create" is built above.

    return plan


# ------------------------------------------------------------------ the apply

def apply_plan(plan: list[Change], cloud: Path = CLOUD_DIR) -> None:
    cloud.mkdir(parents=True, exist_ok=True)
    for change in plan:
        target = cloud / f"{change.name}.json"
        if change.action in ("create", "update"):
            target.write_text(json.dumps(change.after, indent=2) + "\n")
        elif change.action == "delete":
            # TODO (Lab 0, exercise C): remove the resource file from the cloud.
            raise NotImplementedError("delete is not implemented yet")


# ------------------------------------------------------------------- printing

SYMBOL = {"create": "+", "update": "~", "delete": "-"}


def print_plan(plan: list[Change]) -> None:
    if not plan:
        print("No changes. Actual state matches desired state.")
        return
    for c in plan:
        print(f"  {SYMBOL[c.action]} {c.action:<6} {c.name}")
        if c.action == "update":
            for key in sorted(set(c.before or {}) | set(c.after or {})):
                old, new = (c.before or {}).get(key), (c.after or {}).get(key)
                if old != new:
                    print(f"        {key}: {json.dumps(old)} -> {json.dumps(new)}")
    counts = {a: sum(1 for c in plan if c.action == a) for a in SYMBOL}
    print(f"\nPlan: {counts['create']} to create, {counts['update']} to update, "
          f"{counts['delete']} to delete.")


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else "plan"
    desired, actual = load_desired(), load_actual()

    if cmd == "show":
        print(json.dumps(actual, indent=2) if actual else "(fake cloud is empty)")
        return 0

    plan = compute_plan(desired, actual)
    print_plan(plan)

    if cmd == "plan":
        return 0
    if cmd == "apply":
        if plan:
            apply_plan(plan)
            print("\nApply complete.")
        return 0

    print(f"unknown command: {cmd}  (use plan | apply | show)", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
