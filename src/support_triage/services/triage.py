import logging
from dataclasses import asdict, dataclass
from typing import Protocol

from support_triage.core.config import settings


LOGGER = logging.getLogger(__name__)

CATEGORY_TO_TEAM = {
    "billing": "Billing Operations",
    "technical": "Technical Support",
    "account_access": "Identity and Access",
    "general": "Customer Success",
}


class JsonGenerator(Protocol):
    def generate_json(self, prompt: str) -> dict:
        pass


@dataclass(frozen=True)
class TriageResult:
    category: str
    priority: str
    sentiment: str
    confidence: float
    assigned_team: str
    summary: str
    recommended_action: str
    model_name: str

    def as_dict(self) -> dict:
        return asdict(self)


def build_prompt(subject: str, body: str) -> str:
    return f"""
You are a customer support triage assistant.

Classify the support ticket and return only valid JSON with these fields:
category: one of billing, technical, account_access, general
priority: one of low, medium, high
sentiment: one of negative, neutral, positive
confidence: number between 0 and 1
summary: one short sentence
recommended_action: one short sentence for the support agent

Ticket subject: {subject}
Ticket body: {body}
""".strip()


def normalize_result(payload: dict, subject: str, body: str, model_name: str) -> TriageResult:
    category = str(payload.get("category", "general")).strip().lower()
    if category not in CATEGORY_TO_TEAM:
        category = "general"

    priority = str(payload.get("priority", "medium")).strip().lower()
    if priority not in {"low", "medium", "high"}:
        priority = "medium"

    sentiment = str(payload.get("sentiment", "neutral")).strip().lower()
    if sentiment not in {"negative", "neutral", "positive"}:
        sentiment = "neutral"

    try:
        confidence = float(payload.get("confidence", 0.6))
    except (TypeError, ValueError):
        confidence = 0.6
    confidence = max(0.0, min(confidence, 1.0))

    summary = str(payload.get("summary") or f"{subject}: {body[:120]}").strip()
    recommended_action = str(
        payload.get("recommended_action")
        or "Review the ticket details and respond with the next support step."
    ).strip()

    return TriageResult(
        category=category,
        priority=priority,
        sentiment=sentiment,
        confidence=confidence,
        assigned_team=CATEGORY_TO_TEAM[category],
        summary=summary,
        recommended_action=recommended_action,
        model_name=model_name,
    )


def rules_fallback(subject: str, body: str) -> TriageResult:
    text = f"{subject} {body}".lower()

    if any(word in text for word in ["invoice", "billing", "charged", "payment", "refund", "subscription"]):
        category = "billing"
    elif any(word in text for word in ["error", "api", "timeout", "bug", "500", "401", "webhook", "slow"]):
        category = "technical"
    elif any(word in text for word in ["login", "password", "account", "user", "access"]):
        category = "account_access"
    else:
        category = "general"

    if any(word in text for word in ["urgent", "production", "down", "blocked", "end of day", "failed"]):
        priority = "high"
    elif any(word in text for word in ["soon", "renewal", "duplicate", "slow"]):
        priority = "medium"
    else:
        priority = "low"

    sentiment = "negative" if any(word in text for word in ["cannot", "failed", "error", "charged twice"]) else "neutral"

    return TriageResult(
        category=category,
        priority=priority,
        sentiment=sentiment,
        confidence=0.55,
        assigned_team=CATEGORY_TO_TEAM[category],
        summary=f"{subject}. {body[:140]}",
        recommended_action="Validate the customer impact and follow the team playbook.",
        model_name="rules-fallback",
    )


def triage_ticket(subject: str, body: str, client: JsonGenerator | None = None) -> TriageResult:
    if client is None:
        from support_triage.services.ollama import OllamaClient

        client = OllamaClient()
    prompt = build_prompt(subject, body)

    try:
        payload = client.generate_json(prompt)
        return normalize_result(payload, subject, body, settings.ollama_model)
    except Exception as exc:
        LOGGER.warning("Ollama triage failed; using rules fallback: %s", exc)
        return rules_fallback(subject, body)
