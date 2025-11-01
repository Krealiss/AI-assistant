"""Telegram interaction handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

from .pc_control import PCController
from .ollama import OllamaClient

if TYPE_CHECKING:  # pragma: no cover - typing only
    from telebot import TeleBot
else:  # pragma: no cover - TeleBot type only used for hints
    TeleBot = Any


def register_handlers(
    bot: "TeleBot", pc_controller: PCController, ollama_client: Optional[OllamaClient] = None
) -> None:
    """Register command handlers on the provided bot instance."""

    @bot.message_handler(commands=["start", "help"])
    def handle_start(message: Any) -> None:
        bot.reply_to(
            message,
            (
                "👋 Hi! I'm your desktop assistant.\n"
                "Use /open <app>, /shell <command>, or /screenshot to control the PC."
            ),
        )

    @bot.message_handler(commands=["open"])
    def handle_open(message: Any) -> None:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "Please provide the application name, e.g. /open notepad")
            return

        result = pc_controller.open_application(parts[1])
        bot.reply_to(message, f"Opening {parts[1]}... Status: {result['status']}")

    @bot.message_handler(commands=["shell"])
    def handle_shell(message: Any) -> None:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            bot.reply_to(message, "Please provide a shell command, e.g. /shell dir")
            return

        result = pc_controller.run_shell_command(parts[1])
        bot.reply_to(message, f"Command queued. Status: {result['status']}")

    @bot.message_handler(commands=["screenshot"])
    def handle_screenshot(message: Any) -> None:
        result = pc_controller.capture_screenshot()
        bot.reply_to(message, f"Screenshot requested. Status: {result['status']}")

    @bot.message_handler(func=lambda _message: True)
    def handle_fallback(message: Any) -> None:
        if not ollama_client:
            bot.reply_to(
                message,
                "I didn't understand that. Try /help for a list of supported commands.",
            )
            return

        try:
            response = ollama_client.generate(message.text)
        except RuntimeError as exc:
            bot.reply_to(
                message,
                "⚠️ I'm having trouble reaching the Ollama service right now. Please try again later.",
            )
            return

        bot.reply_to(message, response or "I'm not sure how to help with that yet.")


__all__ = ["register_handlers"]
