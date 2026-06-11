# Runbook

## Start The Project

```powershell
ollama pull llama3.1:8b
docker compose up --build
```

## Submit A Demo Ticket

```powershell
python scripts/seed_ticket.py
```

## Open Services

- API docs: `http://localhost:8000/docs`
- MLflow: `http://localhost:5000`
- RabbitMQ: `http://localhost:15672`

RabbitMQ default credentials are `guest` / `guest`.

## Train The Baseline Model

```powershell
docker compose exec api python -m support_triage.ml.train_baseline
```

## Evaluate The Baseline Model

```powershell
docker compose exec api python -m support_triage.ml.evaluate
```

## Common Issues

### Docker command not found

Install Docker Desktop and restart the terminal.

### Ollama model not found

Pull the configured model:

```powershell
ollama pull llama3.1:8b
```

Or update `OLLAMA_MODEL` in `.env`.

### Worker is running but tickets stay queued

Check RabbitMQ:

```powershell
docker compose logs worker
docker compose logs rabbitmq
```
