"""Autograded tests for Lab 0, exercise C.

Run locally with:  make test
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "demo" / "declarative"))

from reconcile import apply_plan, compute_plan, load_actual  # noqa: E402

VM = {"name": "web-1", "type": "vm", "properties": {"size": "small"}}
VM_BIG = {"name": "web-1", "type": "vm", "properties": {"size": "large"}}
NET = {"name": "net", "type": "network", "properties": {"cidr": "10.0.0.0/16"}}


def actions(plan):
    return sorted((c.action, c.name) for c in plan)


def test_empty_cloud_creates_everything():
    plan = compute_plan({"web-1": VM, "net": NET}, {})
    assert actions(plan) == [("create", "net"), ("create", "web-1")]


def test_identical_state_is_a_noop():
    assert compute_plan({"web-1": VM}, {"web-1": VM}) == []


def test_drift_is_an_update():
    plan = compute_plan({"web-1": VM}, {"web-1": VM_BIG})
    assert actions(plan) == [("update", "web-1")]


def test_resource_removed_from_desired_is_deleted():
    plan = compute_plan({"web-1": VM}, {"web-1": VM, "net": NET})
    assert actions(plan) == [("delete", "net")]


def test_apply_twice_is_idempotent(tmp_path):
    desired = {"web-1": VM, "net": NET}
    apply_plan(compute_plan(desired, load_actual(tmp_path)), tmp_path)
    second = compute_plan(desired, load_actual(tmp_path))
    assert second == [], "second apply should have nothing to do"


def test_apply_converges_after_removal(tmp_path):
    apply_plan(compute_plan({"web-1": VM, "net": NET}, {}), tmp_path)
    apply_plan(compute_plan({"web-1": VM}, load_actual(tmp_path)), tmp_path)
    assert sorted(p.name for p in tmp_path.glob("*.json")) == ["web-1.json"]
    assert json.loads((tmp_path / "web-1.json").read_text()) == VM
