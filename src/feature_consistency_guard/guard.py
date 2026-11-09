from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Finding:
    rule_id: str
    status: str
    severity: str
    message: str


@dataclass(frozen=True)
class Evaluation:
    decision: str
    score: int
    passed: int
    total: int
    findings: tuple[Finding, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "score": self.score,
            "passed": self.passed,
            "total": self.total,
            "findings": [asdict(item) for item in self.findings],
        }


def _get(document: dict[str, Any], path: str, default: Any = None) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return current


def _finding(rule_id: str, passed: bool, severity: str, message: str) -> Finding:
    return Finding(rule_id, "PASS" if passed else "FAIL", severity, message)


def evaluate_contract(contract: dict[str, Any]) -> Evaluation:
    """Evaluate a feature contract without network calls or model inference."""
    findings: list[Finding] = []

    required_identity = all(
        _get(contract, path)
        for path in ("feature_view.name", "feature_view.version", "feature_view.entity_key")
    )
    findings.append(_finding("FG-001", required_identity, "BLOCK", "Feature view identity and entity key are declared."))

    offline_schema = _get(contract, "schemas.offline", {})
    online_schema = _get(contract, "schemas.online", {})
    findings.append(_finding("FG-002", bool(offline_schema) and offline_schema == online_schema, "BLOCK", "Offline and online schemas have exact name/type parity."))

    transform_version = _get(contract, "transformation.git_sha", "")
    findings.append(_finding("FG-003", isinstance(transform_version, str) and len(transform_version) >= 7, "BLOCK", "Transformation code is pinned to an immutable revision."))

    findings.append(_finding("FG-004", _get(contract, "offline.point_in_time_join") is True, "BLOCK", "Training retrieval requires point-in-time-correct joins."))

    max_age = _get(contract, "freshness.max_age_minutes", -1)
    observed_age = _get(contract, "freshness.observed_age_minutes", 10**9)
    freshness_ok = isinstance(max_age, (int, float)) and max_age > 0 and observed_age <= max_age
    findings.append(_finding("FG-005", freshness_ok, "BLOCK", "Observed feature age is within its freshness SLO."))

    ttl = _get(contract, "online.ttl_minutes", -1)
    ttl_ok = isinstance(ttl, (int, float)) and ttl >= max_age > 0
    findings.append(_finding("FG-006", ttl_ok, "BLOCK", "Online TTL is explicit and no shorter than the freshness window."))

    p95 = _get(contract, "online.observed_p95_latency_ms", 10**9)
    latency_slo = _get(contract, "online.p95_latency_slo_ms", -1)
    findings.append(_finding("FG-007", latency_slo > 0 and p95 <= latency_slo, "REVIEW", "Online serving p95 latency meets its SLO."))

    availability = _get(contract, "online.observed_availability_percent", 0)
    availability_slo = _get(contract, "online.availability_slo_percent", 100)
    findings.append(_finding("FG-008", availability >= availability_slo, "REVIEW", "Online store availability meets its SLO."))

    skew = _get(contract, "parity.observed_mismatch_percent", 100)
    skew_limit = _get(contract, "parity.max_mismatch_percent", -1)
    findings.append(_finding("FG-009", skew_limit >= 0 and skew <= skew_limit, "BLOCK", "Sampled offline/online mismatch is within policy."))

    sample_size = _get(contract, "parity.sample_size", 0)
    minimum_sample = _get(contract, "parity.minimum_sample_size", 1)
    findings.append(_finding("FG-010", minimum_sample > 0 and sample_size >= minimum_sample, "REVIEW", "Parity evidence meets the minimum sample size."))

    interval = _get(contract, "materialization.interval_minutes", 10**9)
    findings.append(_finding("FG-011", max_age > 0 and interval <= max_age, "BLOCK", "Materialization cadence can meet the freshness SLO."))

    findings.append(_finding("FG-012", _get(contract, "materialization.backfill_idempotent") is True, "BLOCK", "Backfills are declared idempotent."))

    encrypted = _get(contract, "security.encryption_at_rest") is True and _get(contract, "security.encryption_in_transit") is True
    findings.append(_finding("FG-013", encrypted, "BLOCK", "Feature data is encrypted in transit and at rest."))

    access_ok = _get(contract, "security.least_privilege_rbac") is True and bool(_get(contract, "security.data_classification"))
    findings.append(_finding("FG-014", access_ok, "BLOCK", "Least-privilege access and data classification are defined."))

    operations_ok = all(_get(contract, path) for path in ("operations.owner", "operations.runbook", "operations.alert_route"))
    findings.append(_finding("FG-015", operations_ok, "REVIEW", "An owner, runbook, and alert route are declared."))

    human_gate = _get(contract, "promotion.human_approval_required") is True
    findings.append(_finding("FG-016", human_gate, "BLOCK", "Promotion requires an explicit human approval gate."))

    passed = sum(item.status == "PASS" for item in findings)
    score = round(100 * passed / len(findings))
    failures = [item for item in findings if item.status == "FAIL"]
    if any(item.severity == "BLOCK" for item in failures):
        decision = "BLOCK"
    elif failures:
        decision = "REVIEW"
    else:
        decision = "PASS"
    return Evaluation(decision, score, passed, len(findings), tuple(findings))
