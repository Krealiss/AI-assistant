"""Configuration utilities for the assistant package."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Config:
    """Holds configuration values required by the assistant."""

    telegram_bot_token: str
    openai_api_key: Optional[str] = None
    pc_control_endpoint: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        """Build configuration from environment variables.

        Raises:
            RuntimeError: If the Telegram bot token is missing.
        """

        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise RuntimeError(
                "The TELEGRAM_BOT_TOKEN environment variable must be set before starting the assistant."
            )

        return cls(
            telegram_bot_token=token,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            pc_control_endpoint=os.getenv("PC_CONTROL_ENDPOINT"),
        )


__all__ = ["Config"]
