from fastapi import APIRouter, Request, HTTPException
from app import settings
from app.webhooks.utils import extract_webhook_data, verify_signature, verify_timestamp
from app.schemas.webhooks import (
    OrderCreatedWebhook,
    OrderUpdatedWebhook,
    OrderCancelledWebhook,
    PaymentSuccessfulWebhook,
    PaymentFailedWebhook,
)

router = APIRouter()


async def handle_webhook(request: Request, secret: str, webhook_name: str, model=None):
    """
    Generic webhook handler to reduce repeated code.
    If a Pydantic model is provided, parse the JSON into the model.
    """
    timestamp, signature, body = await extract_webhook_data(request)

    # Verify timestamp and signature
    verify_timestamp(timestamp)
    verify_signature(secret, timestamp, body, signature)

    # Parse JSON
    try:
        json_body = body.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Validate with Pydantic model if provided
    if model:
        try:
            payload = model.parse_raw(body)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid payload: {e}")
        print(f"{webhook_name} Webhook:", payload)
    else:
        payload = json_body
        print(f"{webhook_name} Webhook:", payload)

    return {"message": f"{webhook_name} webhook received and verified", "data": payload}


# ----------------------------
# Webhook routes
# ----------------------------

@router.post("/order-created")
async def order_created_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.CREATE_ORDER_WEBHOOK_SECRET,
        webhook_name="Order Created",
        model=OrderCreatedWebhook
    )


@router.post("/order-updated")
async def order_updated_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.UPDATE_ORDER_WEBHOOK_SECRET,
        webhook_name="Order Updated",
        model=OrderUpdatedWebhook
    )


@router.post("/order-cancel")
async def order_cancel_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.CANCEL_ORDER_WEBHOOK_SECRET,
        webhook_name="Order Cancel",
        model=OrderCancelledWebhook
    )


@router.post("/payment-successful")
async def payment_successful_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_SUCCESSFUL_WEBHOOK_SECRET,
        webhook_name="Payment Successful",
        model=PaymentSuccessfulWebhook
    )


@router.post("/payment-failed")
async def payment_failed_webhook(request: Request):
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_FAILED_WEBHOOK_SECRET,
        webhook_name="Payment Failed",
        model=PaymentFailedWebhook
    )
