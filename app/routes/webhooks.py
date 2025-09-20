from fastapi import APIRouter, Request, HTTPException
from app import settings
from app.webhooks import (
    extract_webhook_data,
    verify_signature,
    verify_timestamp,
    events,
    WebhookMeta
)
from app.schemas.webhooks import (
    OrderCreatedWebhook,
    OrderUpdatedWebhook,
    OrderCancelledWebhook,
    PaymentSuccessfulWebhook,
    PaymentFailedWebhook,
)

router = APIRouter()


async def handle_webhook(request: Request, secret: str, event_name: str, model=None):
    """
    Generic webhook handler for all events.
    If a Pydantic model is provided, parse the JSON into the model.
    """
    timestamp, signature, body = await extract_webhook_data(request)

    verify_timestamp(timestamp)
    verify_signature(secret, timestamp, body, signature)

    try:
        json_body = body.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if model:
        payload = model.parse_raw(body)
    else:
        payload = json_body

    event_payload = getattr(payload, "data", payload)

    meta: WebhookMeta = {"timestamp": timestamp, "event": event_name}
    await events.dispatch(event_name, event_payload, meta)

    return {"message": f"{event_name} webhook received and verified", "data": payload}


@router.post("/order-created")
async def order_created_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.CREATE_ORDER_WEBHOOK_SECRET,
        event_name="order.created",
        model=OrderCreatedWebhook
    )


@router.post("/order-updated")
async def order_updated_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.UPDATE_ORDER_WEBHOOK_SECRET,
        event_name="order.updated",
        model=OrderUpdatedWebhook
    )


@router.post("/order-cancelled")
async def order_cancelled_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.CANCEL_ORDER_WEBHOOK_SECRET,
        event_name="order.cancelled",
        model=OrderCancelledWebhook
    )


@router.post("/payment-successful")
async def payment_successful_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_SUCCESSFUL_WEBHOOK_SECRET,
        event_name="payment.successful",
        model=PaymentSuccessfulWebhook
    )


@router.post("/payment-failed")
async def payment_failed_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_FAILED_WEBHOOK_SECRET,
        event_name="payment.failed",
        model=PaymentFailedWebhook
    )
