import json
from typing import Any

import requests

from support_triage.core.config import settings


class OllamaClient:
    def __init__(self, base_url: str = settings.ollama_base_url, model: str = settings.ollama_model) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate_json(self, prompt: str) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "format": "json",
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        raw = data.get("response", "{}")
        return json.loads(raw)
