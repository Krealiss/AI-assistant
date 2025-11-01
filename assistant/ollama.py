"""Lightweight client for interacting with an Ollama server."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict
from urllib import request, error

LOGGER = logging.getLogger(__name__)


@dataclass
class OllamaClient:
    """Wrapper around the Ollama HTTP API."""

    model: str
    base_url: str = "http://localhost:11434"

    def generate(self, prompt: str, **options: Any) -> str:
        """Generate a response from the configured Ollama model.

        Args:
            prompt: The prompt to send to the model.
            **options: Additional JSON-serialisable options forwarded to the API.

        Returns:
            The text response produced by the model.

        Raises:
            RuntimeError: If the Ollama service cannot be reached or responds with an error.
        """

        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        payload.update(options)

        data = json.dumps(payload).encode("utf-8")
        endpoint = f"{self.base_url.rstrip('/')}/api/generate"
        req = request.Request(endpoint, data=data, headers={"Content-Type": "application/json"})

        try:
            with request.urlopen(req, timeout=30) as response:
                body = response.read()
        except error.URLError as exc:  # pragma: no cover - networking failure path
            LOGGER.error("Failed to reach Ollama at %s: %s", endpoint, exc)
            raise RuntimeError("Failed to contact the Ollama service") from exc

        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as exc:  # pragma: no cover - defensive guard
            LOGGER.error("Ollama responded with invalid JSON: %s", body)
            raise RuntimeError("Received invalid response from Ollama") from exc

        if "response" not in parsed:
            LOGGER.error("Unexpected Ollama payload: %s", parsed)
            raise RuntimeError("Unexpected response structure from Ollama")

        return str(parsed["response"]).strip()


__all__ = ["OllamaClient"]
