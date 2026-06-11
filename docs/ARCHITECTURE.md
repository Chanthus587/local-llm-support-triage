# Architecture

This project is organized as an event-driven AI workflow.

## Runtime Flow

1. A client submits a support ticket to the FastAPI service.
2. The API stores ticket metadata in PostgreSQL.
3. The API stores the raw ticket body in MongoDB.
4. The API publishes a ticket id to RabbitMQ.
5. The worker consumes the message and loads the ticket context.
6. The worker calls Ollama for classification, summary, priority, sentiment, and recommended action.
7. If Ollama is unavailable, the worker uses a rules-based fallback.
8. The worker stores structured predictions in PostgreSQL and the raw model payload in MongoDB.
9. Metrics endpoints expose ticket status and prediction distribution.

## Main Packages

```text
src/support_triage/
├── api/          FastAPI routes
├── core/         configuration and logging
├── db/           SQLAlchemy models plus Mongo helpers
├── messaging/    RabbitMQ producer and consumer helpers
├── ml/           MLflow baseline model training and evaluation
├── schemas/      Pydantic request/response models
├── services/     business logic and LLM triage logic
└── workers/      background queue consumers
```

## Storage Choice

- PostgreSQL stores normalized operational data: ticket metadata, status, and predictions.
- MongoDB stores unstructured or semi-structured data: raw ticket bodies and full LLM payloads.
- RabbitMQ decouples API latency from LLM inference latency.
- MLflow tracks experiments and metrics for traditional ML baselines.

## Failure Handling

- If Ollama fails, triage uses a deterministic rules fallback.
- If a ticket body is missing from MongoDB, the worker marks the ticket as `failed`.
- Queue messages are acknowledged only after processing succeeds.
