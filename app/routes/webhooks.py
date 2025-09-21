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
    WebhookResponse,
)

router = APIRouter(
    prefix="/ghala/webhook",
    tags=["Webhooks"],
    responses={404: {"description": "Not found"}},
)

async def handle_webhook(request: Request, secret: str, event_name: str, model=None) -> WebhookResponse:
    """
    Generic webhook handler for all Ghala events.

    This function:
    1. Extracts timestamp, signature, and body from the request.
    2. Verifies the timestamp and HMAC signature.
    3. Parses the payload using a Pydantic model if provided.
    4. Dispatches the event to any registered plugin handlers.
    5. Returns a standardized acknowledgment.

    Args:
        request (Request): FastAPI request object.
        secret (str): Webhook secret for signature verification.
        event_name (str): Name of the event to dispatch, e.g., "order.created".
        model (Optional[PydanticModel]): Optional Pydantic model to parse the request body.

    Returns:
        WebhookResponse: Standard acknowledgment response.

    Raises:
        HTTPException: If JSON is invalid or payload fails validation.
    """
    timestamp, signature, body = await extract_webhook_data(request)

    # Verify request authenticity
    verify_timestamp(timestamp)
    verify_signature(secret, timestamp, body, signature)

    try:
        json_body = body.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    # Parse payload with Pydantic model if provided
    if model:
        try:
            payload = model.parse_raw(body)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid payload: {e}")
    else:
        payload = json_body

    # Extract actual event data
    event_payload = getattr(payload, "data", payload)
    meta: WebhookMeta = {"timestamp": timestamp, "event": event_name}

    # Dispatch event to plugins
    await events.dispatch(event_name, event_payload, meta)

    # Return acknowledgment
    return WebhookResponse(message=f"{event_name} webhook received and verified")


@router.post("/order-created", response_model=WebhookResponse)
async def order_created(request: Request):
    """
    Handle 'order.created' webhook.

    Args:
        request (Request): Incoming HTTP request from Ghala.

    Returns:
        WebhookResponse: Confirmation of successful processing.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.CREATE_ORDER_WEBHOOK_SECRET,
        event_name="order.created",
        model=OrderCreatedWebhook
    )


@router.post("/order-updated", response_model=WebhookResponse)
async def order_updated(request: Request):
    """
    Handle 'order.updated' webhook.

    Args:
        request (Request): Incoming HTTP request from Ghala.

    Returns:
        WebhookResponse: Confirmation of successful processing.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.UPDATE_ORDER_WEBHOOK_SECRET,
        event_name="order.updated",
        model=OrderUpdatedWebhook
    )


@router.post("/order-cancelled", response_model=WebhookResponse)
async def order_cancelled(request: Request):
    """
    Handle 'order.cancelled' webhook.

    Args:
        request (Request): Incoming HTTP request from Ghala.

    Returns:
        WebhookResponse: Confirmation of successful processing.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.CANCEL_ORDER_WEBHOOK_SECRET,
        event_name="order.cancelled",
        model=OrderCancelledWebhook
    )


@router.post("/payment-successful", response_model=WebhookResponse)
async def payment_successful(request: Request):
    """
    Handle 'payment.successful' webhook.

    Args:
        request (Request): Incoming HTTP request from Ghala.

    Returns:
        WebhookResponse: Confirmation of successful processing.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_SUCCESSFUL_WEBHOOK_SECRET,
        event_name="payment.successful",
        model=PaymentSuccessfulWebhook
    )


@router.post("/payment-failed", response_model=WebhookResponse)
async def payment_failed(request: Request):
    """
    Handle 'payment.failed' webhook.

    Args:
        request (Request): Incoming HTTP request from Ghala.

    Returns:
        WebhookResponse: Confirmation of successful processing.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_FAILED_WEBHOOK_SECRET,
        event_name="payment.failed",
        model=PaymentFailedWebhook
    )
