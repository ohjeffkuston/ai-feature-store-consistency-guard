# Demand validation — 2026-11-09

## Authoritative technical sources

- [Amazon SageMaker Feature Store storage configurations](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-storage-configurations.html): online inference, historical offline training, and synchronization to avoid discrepancies.
- [Amazon SageMaker Feature Store TTL](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-time-to-live.html): expiration as event time plus TTL and record/feature-group defaults.
- [Amazon SageMaker Feature Store concepts](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-concepts.html): latest-value online behavior and historical offline records.
- [Amazon SageMaker Feature Store security](https://docs.aws.amazon.com/sagemaker/latest/dg/feature-store-security.html): encryption and audit considerations.
- [Google Cloud: serve features from an online store](https://docs.cloud.google.com/vertex-ai/featurestore/latest/serve-feature-values): synchronization before serving plus entity ID and feature timestamp behavior.

## Recurring requirements in live postings

- [Hadrian — ML Platform Engineer](https://jobs.ashbyhq.com/hadrian-automation/18edaac7-95af-4fb6-b25c-b7000911167d): online/offline contract integrity, training-serving skew, Kubernetes, observability, incident response, and production failure modes; $170,000–$300,000.
- [BetterHelp — Staff ML/AI Platform Engineer](https://job-boards.greenhouse.io/betterhelpcom/jobs/5017993008): production ML/AI platforms and feature stores; U.S. remote; $200,000–$245,000.
- [Chime — Senior Software Engineer, ML Platform](https://job-boards.greenhouse.io/chime/jobs/8765684002): feature pipelines, real-time inference, evaluation, observability, governance, privacy, Kubernetes, and on-call.
- [FutureFit AI — Staff ML Platform Engineer](https://jobs.ashbyhq.com/futurefitai/940d6f7e-e901-4580-956b-60481c5ebcdc/): remote U.S./Canada ML-platform ownership; $172,000–$215,000.
- [Whatnot — ML Platform Engineer](https://jobs.ashbyhq.com/whatnot/11162b1e-e7c9-432d-8ef6-6e89d28b3078/): low-latency serving, distributed training, GPU inference, and reproducibility; $245,000–$345,000, hub-constrained.

## Selection rationale

Feature-store consistency is a recurring production responsibility at the intersection of ML infrastructure, data correctness, SRE, security, and platform delivery. It complements dataset lineage and GenAI observability without duplicating either: lineage answers where training data came from; this guard verifies that features used in training and serving remain contractually and operationally equivalent.

The postings validate demand but are not automatically qualifying applications. The strongest examples are staff/senior roles, hub-constrained, or omit a verifiable future-sponsorship policy. No application should be submitted unless the exact role independently passes every standing gate.
