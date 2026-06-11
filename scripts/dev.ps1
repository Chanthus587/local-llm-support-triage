param(
    [ValidateSet("up", "down", "logs", "train", "test")]
    [string]$Command = "up"
)

switch ($Command) {
    "up" { docker compose up --build }
    "down" { docker compose down }
    "logs" { docker compose logs -f api worker }
    "train" { docker compose exec api python -m support_triage.ml.train_baseline }
    "test" { python -m pytest }
}
