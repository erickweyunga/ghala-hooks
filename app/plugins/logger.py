from app.webhooks.events import events
from app.schemas.webhooks import  OrderData

@events.on("*")
async def log_order_created(payload: OrderData, meta):
    print(f"Order created: {payload.order_id}")
    print(f"Order created: {payload}")
