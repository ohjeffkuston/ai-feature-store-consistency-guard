# Deployment and operations guide

## Staged rollout

1. Export metadata and aggregate parity metrics from a sandbox feature view.
2. Run report-only and publish the JSON result as a CI artifact.
3. Exercise the known-bad contract and verify every blocking rule.
4. Shadow the production workflow for at least one release cycle.
5. Define feature-class-specific freshness, TTL, latency, availability, mismatch, and sample thresholds.
6. Enable `BLOCK` enforcement through a reviewed branch rule or GitOps check.
7. Keep final promotion behind a named human approver.

```bash
feature-consistency-guard rendered/feature-contract.yaml --json > decision.json
```

Run in a non-root container with a read-only filesystem. Use workload identity and narrowly scoped read-only permissions. The controller consumes a signed decision; the evaluator cannot modify a Feature Store, Kubernetes object, or cloud resource.

## Security controls

- Exclude raw feature values, tokens, endpoints, and customer identifiers.
- Encrypt evidence and restrict it to platform, security, and model-risk roles.
- Pin and scan the container; sign artifacts with contract, policy, and transformation provenance.
- Separate the collector identity from the approver identity.

## Failure modes and rollback

- Metadata unavailable: fail closed for promotion and leave current serving traffic unchanged.
- Parity monitor delayed: mark evidence stale; never interpret missing data as zero skew.
- Small or biased sample: return `REVIEW` and use stratified sampling.
- Intentional migration: publish a new feature-view version and dual-read it.
- False positives: tune in report-only mode through policy review.
- Guard outage: show the last signed result for visibility only; never authorize a new promotion with it.

Disabling enforcement requires the same review path as enabling it. Preserve failed evidence, revert only to report-only mode, and time-limit any risk acceptance.

## Success measures

Track promotion coverage, ownership/runbook coverage, mismatch breach rate, stale-feature rate, mean time to identify materialization failures, review duration, false-positive rate, and escaped skew incidents. Establish the baseline before claiming improvement.
