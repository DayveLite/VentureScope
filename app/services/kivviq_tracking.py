
import json
import logging
from typing import Any, Optional

from kivviq import EventType
from kivviq.client import (
    Kivviq,
    KivviqHTTPClient,
    install_hooks,
    uninstall_hooks,
)
from kivviq.event import build_event_payload

logger = logging.getLogger(__name__)


class KivviqTracker:
    """Manage one VentureScope execution and its Kivviq events."""

    def __init__(
        self,
        kivviq: Kivviq,
        api_key: str,
        backend_url: str,
        run_name: str = "venturescope-agent",
    ):
        self.run = None
        self.hooks = []
        self.finished = False

        self.http = KivviqHTTPClient(
            api_key=api_key,
            backend_url=backend_url,
        )

        try:
            self.run = kivviq.start_run(name=run_name)

            if self.run is not None:
                self.hooks = install_hooks(self.run)

        except Exception:
            logger.exception("Could not initialize Kivviq tracking.")

    @staticmethod
    def _serialize(value: Any, limit: int = 5000) -> str:
        """Convert event data to bounded JSON text."""

        try:
            result = json.dumps(
                value,
                ensure_ascii=False,
                default=str,
            )
        except Exception:
            result = str(value)

        if len(result) > limit:
            result = result[:limit] + "... [truncated]"

        return result

    def _submit_event(
        self,
        event_type: str,
        name: str,
        payload: dict,
    ) -> bool:
        """Submit a typed event through the public HTTP client."""

        if self.run is None or self.finished:
            return False

        try:
            event_data = build_event_payload(
                event_type=event_type,
                name=name,
                payload=payload,
            )

            response = self.http.post(
                f"/api/v1/runs/{self.run.run_id}/events",
                event_data,
            )

            return response is not None

        except Exception:
            logger.exception(
                "Failed to submit Kivviq event: %s",
                name,
            )
            return False

    def log_tool_call(
        self,
        tool_name: str,
        arguments: dict,
        result: Any,
        duration_ms: float,
    ) -> bool:
        """Record a successfully executed tool."""

        return self._submit_event(
            event_type=EventType.TOOL_CALL,
            name=tool_name,
            payload={
                "arguments": self._serialize(arguments, 2000),
                "result": self._serialize(result, 5000),
                "duration_ms": round(duration_ms, 2),
                "success": True,
            },
        )

    def log_tool_error(
        self,
        tool_name: str,
        arguments: dict,
        error: Exception,
        duration_ms: float,
    ) -> bool:
        """Record a failed tool execution."""

        return self._submit_event(
            event_type=EventType.ERROR,
            name=tool_name,
            payload={
                "arguments": self._serialize(arguments, 2000),
                "error": str(error)[:2000],
                "duration_ms": round(duration_ms, 2),
                "success": False,
            },
        )

    def finish(
        self,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> None:
        """End the run and always uninstall instrumentation hooks."""

        if self.finished:
            return

        self.finished = True

        try:
            if self.run is not None:
                self.run.end(
                    status=status,
                    error_message=error_message,
                )
        except Exception:
            logger.exception("Could not finish Kivviq run.")

        finally:
            try:
                uninstall_hooks(self.hooks)
            except Exception:
                logger.exception("Could not uninstall Kivviq hooks.")

            try:
                self.http.close()
            except Exception:
                logger.exception("Could not close Kivviq HTTP client.")
