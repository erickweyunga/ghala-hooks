from __future__ import annotations

from collections import defaultdict
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Protocol,
    TypedDict,
)


class WebhookMeta(TypedDict, total=False):
    """Metadata passed to webhook handlers."""
    event: str
    timestamp: str
    signature: str


class WebhookHandler(Protocol):
    """Protocol for async webhook handler functions."""
    async def __call__(self, payload: Any, meta: WebhookMeta) -> None: ...


class WebhookEvents:
    def __init__(self) -> None:
        self._handlers: Dict[str, List[WebhookHandler]] = defaultdict(list)

    def on(self, event_name: str) -> Callable[[WebhookHandler], WebhookHandler]:
        """Register a handler for a given event name."""
        def decorator(func: WebhookHandler) -> WebhookHandler:
            self._handlers[event_name].append(func)
            return func
        return decorator

    async def dispatch(self, event_name: str, payload: Any, meta: WebhookMeta) -> None:
        """Dispatch an event to all registered handlers."""
        meta = {**meta, "event": event_name}

        for handler in self._handlers.get(event_name, []):
            await handler(payload, meta)

        for handler in self._handlers.get("*", []):
            await handler(payload, meta)


events = WebhookEvents()
