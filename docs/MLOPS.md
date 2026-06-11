# MLOps Plan

The project starts with simple but clear MLOps practices.

## Current Implementation

- MLflow experiment tracking for a TF-IDF + logistic regression baseline.
- Docker Compose for reproducible local services.
- Model artifacts written to `artifacts/`.
- Operational metrics exposed by `/metrics/summary`.
- Deterministic fallback model for Ollama outages.

## Recommended Next Steps

1. Add a labeled validation set with real ticket examples.
2. Track prompt versions as MLflow parameters.
3. Add regression tests for prompt outputs using saved examples.
4. Add drift checks for category and priority distribution.
5. Add confidence threshold alerts.
6. Add GitHub Actions for tests and Docker image build.
7. Add Prometheus/Grafana dashboards.

## Useful Metrics

- Ticket volume by status
- Category distribution
- Priority distribution
- Average triage latency
- Ollama failure rate
- Rules fallback rate
- Human correction rate
- Baseline model accuracy and macro F1
