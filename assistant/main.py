"""Entry point for the Telegram assistant bot."""

from __future__ import annotations

import logging
from typing import Optional

from telebot import TeleBot

from .config import Config
from .handlers import register_handlers
from .pc_control import PCController
from .ollama import OllamaClient

LOGGER = logging.getLogger(__name__)


def build_bot(
    config: Config,
    pc_controller: Optional[PCController] = None,
    ollama_client: Optional[OllamaClient] = None,
) -> TeleBot:
    """Create and configure the TeleBot instance."""

    controller = pc_controller or PCController(endpoint=config.pc_control_endpoint)
    ollama = ollama_client
    if not ollama and config.ollama_model:
        base_url = config.ollama_base_url or "http://localhost:11434"
        ollama = OllamaClient(model=config.ollama_model, base_url=base_url)

    bot = TeleBot(config.telegram_bot_token, parse_mode="Markdown")
    register_handlers(bot, controller, ollama)
    return bot


def run() -> None:
    """Boot the assistant using configuration from the environment."""

    logging.basicConfig(level=logging.INFO)
    config = Config.from_env()
    LOGGER.info("Starting assistant with endpoint=%s", config.pc_control_endpoint)
    if config.ollama_model:
        LOGGER.info(
            "Ollama integration enabled with model=%s base_url=%s",
            config.ollama_model,
            config.ollama_base_url or "http://localhost:11434",
        )
    bot = build_bot(config)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    run()
