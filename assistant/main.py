"""Entry point for the Telegram assistant bot."""

from __future__ import annotations

import logging
from typing import Optional

from telebot import TeleBot

from .config import Config
from .handlers import register_handlers
from .pc_control import PCController

LOGGER = logging.getLogger(__name__)


def build_bot(config: Config, pc_controller: Optional[PCController] = None) -> TeleBot:
    """Create and configure the TeleBot instance."""

    controller = pc_controller or PCController(endpoint=config.pc_control_endpoint)
    bot = TeleBot(config.telegram_bot_token, parse_mode="Markdown")
    register_handlers(bot, controller)
    return bot


def run() -> None:
    """Boot the assistant using configuration from the environment."""

    logging.basicConfig(level=logging.INFO)
    config = Config.from_env()
    LOGGER.info("Starting assistant with endpoint=%s", config.pc_control_endpoint)
    bot = build_bot(config)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    run()
