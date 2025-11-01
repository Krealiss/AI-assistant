"""Desktop control interfaces used by the assistant."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class PCController:
    """Facade for desktop control actions.

    The implementation intentionally remains lightweight so that it can be
    expanded with real automation tooling (e.g. gRPC, REST, or local scripts)
    without changing the bot-facing API.
    """

    endpoint: Optional[str] = None

    def send_command(self, name: str, **payload: Any) -> Dict[str, Any]:
        """Send a command to the PC control service.

        This stub prints the command and returns a mock response. Replace this
        with real networking logic to integrate with a desktop automation
        service.
        """

        message = {"command": name, "payload": payload, "endpoint": self.endpoint}
        # In a real implementation this would be an HTTP/gRPC request.
        print(f"[PCController] sending: {json.dumps(message, ensure_ascii=False)}")
        return {"status": "queued", "command": name, "payload": payload}

    def open_application(self, application: str) -> Dict[str, Any]:
        """Request opening an application on the remote desktop."""

        return self.send_command("open_application", application=application)

    def run_shell_command(self, command: str) -> Dict[str, Any]:
        """Request execution of an arbitrary shell command."""

        return self.send_command("run_shell_command", command=command)

    def capture_screenshot(self) -> Dict[str, Any]:
        """Request a screenshot capture from the remote desktop."""

        return self.send_command("capture_screenshot")


__all__ = ["PCController"]
