from app.webhooks.events import events
from app.schemas.webhooks import OrderData
from app.webhooks.events import WebhookMeta

PLUGIN_ACTIVE = True

@events.on("*")
async def log_all_events(payload: OrderData, meta: WebhookMeta) -> None:
    event_name = meta.get("event", "unknown")

    print(f"[{event_name}] Order ID: {payload.order_id}")
    print(f"[{event_name}] Payload: {payload}")
