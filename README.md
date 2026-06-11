# Local LLM Customer Support Ticket Triage

Production-style portfolio project for AI support automation using **Ollama**, **FastAPI**, **PostgreSQL**, **MongoDB**, **RabbitMQ**, and **MLflow**.

The system accepts customer support tickets, stores structured data in SQL, stores raw text and LLM payloads in NoSQL, queues triage jobs, processes them with a local LLM, and tracks a baseline ML model with MLflow.

## Features

- Ticket ingestion API with FastAPI
- Async processing with RabbitMQ
- Local LLM classification through Ollama
- Rules fallback when Ollama is unavailable
- PostgreSQL for ticket metadata and predictions
- MongoDB for raw ticket text and full model outputs
- MLflow baseline model tracking
- Operational metrics endpoint
- Tests and structured docs

## Project Structure

```text
.
├── data/                     sample training data
├── docs/                     architecture, runbook, MLOps plan
├── scripts/                  local helper scripts
├── src/support_triage/
│   ├── api/                  FastAPI routes
│   ├── core/                 config and logging
│   ├── db/                   PostgreSQL and MongoDB access
│   ├── messaging/            RabbitMQ helpers
│   ├── ml/                   MLflow training/evaluation
│   ├── schemas/              Pydantic models
│   ├── services/             business logic and LLM triage
│   └── workers/              background consumers
├── tests/                    unit tests
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```

## Architecture

```text
Client -> FastAPI -> PostgreSQL
                  -> MongoDB
                  -> RabbitMQ -> Worker -> Ollama
                                      -> PostgreSQL/MongoDB

MLflow tracks baseline ML experiments.
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the detailed design.

## Prerequisites

- Docker Desktop
- Ollama installed locally
- Python 3.11 if running tests outside Docker

Pull a local model:

```powershell
ollama pull llama3.1:8b
```

## Run

```powershell
docker compose up --build
```

Open:

- API docs: `http://localhost:8000/docs`
- MLflow: `http://localhost:5000`
- RabbitMQ: `http://localhost:15672`

## Submit A Ticket

```powershell
Invoke-RestMethod -Method Post http://localhost:8000/tickets `
  -ContentType "application/json" `
  -Body '{
    "customer_id": "cust-102",
    "subject": "Cannot access billing dashboard",
    "body": "Our admin account gets a 500 error every time we open billing. We need invoices before end of day.",
    "channel": "email"
  }'
```

Check status:

```powershell
Invoke-RestMethod http://localhost:8000/tickets/1
```

Check metrics:

```powershell
Invoke-RestMethod http://localhost:8000/metrics/summary
```

## MLOps

Train the baseline classifier:

```powershell
docker compose exec api python -m support_triage.ml.train_baseline
```

Evaluate it:

```powershell
docker compose exec api python -m support_triage.ml.evaluate
```

See [docs/MLOPS.md](docs/MLOPS.md) for the improvement plan.

## Local Developer Commands

```powershell
python -m pytest
$env:PYTHONPATH='src'; python -m unittest discover -s tests
python -m compileall src scripts tests
.\scripts\dev.ps1 up
.\scripts\dev.ps1 logs
```
