# AI Assistant

A lightweight Telegram bot that bridges chat commands to PC automation tasks. It can optionally forward free-form text prompts to an [Ollama](https://ollama.com/) server for natural-language responses.

## Configuration

Set the following environment variables before launching the bot:

- `TELEGRAM_BOT_TOKEN` (**required**): API token for your Telegram bot.
- `PC_CONTROL_ENDPOINT` (optional): URL for the desktop automation backend.
- `OLLAMA_MODEL` (optional): Name of the Ollama model to use for conversational responses.
- `OLLAMA_BASE_URL` (optional): Base URL of the Ollama server (defaults to `http://localhost:11434`).

Only when `OLLAMA_MODEL` is provided will the bot forward non-command messages to the Ollama service.

## Running

```bash
pip install -r requirements.txt
python -m assistant.main
```

The bot runs with long polling and will log when Ollama support is enabled.
