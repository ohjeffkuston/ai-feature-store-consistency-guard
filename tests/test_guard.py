from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from feature_consistency_guard.guard import evaluate_contract


SAMPLE = Path(__file__).parents[1] / "samples" / "compliant-contract.yaml"


@pytest.fixture()
def contract():
    return yaml.safe_load(SAMPLE.read_text())


def test_compliant_contract_passes_all_checks(contract):
    result = evaluate_contract(contract)
    assert result.decision == "PASS"
    assert result.score == 100
    assert result.passed == result.total == 16


@pytest.mark.parametrize(
    ("path", "value", "rule_id"),
    [
        ("feature_view.entity_key", "", "FG-001"),
        ("schemas.online.transaction_velocity_1h", "string", "FG-002"),
        ("transformation.git_sha", "main", "FG-003"),
        ("offline.point_in_time_join", False, "FG-004"),
        ("freshness.observed_age_minutes", 31, "FG-005"),
        ("online.ttl_minutes", 29, "FG-006"),
        ("parity.observed_mismatch_percent", 0.6, "FG-009"),
        ("materialization.interval_minutes", 31, "FG-011"),
        ("materialization.backfill_idempotent", False, "FG-012"),
        ("security.encryption_in_transit", False, "FG-013"),
        ("security.least_privilege_rbac", False, "FG-014"),
        ("promotion.human_approval_required", False, "FG-016"),
    ],
)
def test_blocking_failures_block(contract, path, value, rule_id):
    changed = deepcopy(contract)
    target = changed
    parts = path.split(".")
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value
    result = evaluate_contract(changed)
    assert result.decision == "BLOCK"
    assert next(item for item in result.findings if item.rule_id == rule_id).status == "FAIL"


def test_latency_failure_requires_review(contract):
    contract["online"]["observed_p95_latency_ms"] = 21
    result = evaluate_contract(contract)
    assert result.decision == "REVIEW"


def test_missing_operations_require_review(contract):
    contract["operations"]["runbook"] = ""
    result = evaluate_contract(contract)
    assert result.decision == "REVIEW"


def test_serialized_result_is_stable(contract):
    data = evaluate_contract(contract).to_dict()
    assert list(data) == ["decision", "score", "passed", "total", "findings"]
    assert data["findings"][0]["rule_id"] == "FG-001"
