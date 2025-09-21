from fastapi import APIRouter, Request, HTTPException
from app import settings
from app.webhooks import (
    extract_webhook_data,
    verify_signature,
    verify_timestamp,
    events,
    WebhookMeta,
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
    2. Verifies the timestamp and HMAC signature to ensure authenticity.
    3. Parses the payload using a Pydantic model if provided.
    4. Dispatches the event to any registered plugin handlers.
    5. Returns a standardized acknowledgment.

    Args:
        request (Request): The raw HTTP request object from Ghala.
        secret (str): Webhook secret for signature verification.
        event_name (str): Name of the event to dispatch (e.g., "order.created").
        model (Optional[PydanticModel]): Pydantic model to validate the incoming payload.

    Returns:
        WebhookResponse: A confirmation response indicating successful receipt.

    Raises:
        HTTPException: If request verification fails or payload is invalid.
    """
    timestamp, signature, body = await extract_webhook_data(request)

    verify_timestamp(timestamp)
    verify_signature(secret, timestamp, body, signature)

    try:
        json_body = body.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    if model:
        try:
            payload = model.parse_raw(body)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid payload: {e}")
    else:
        payload = json_body

    event_payload = getattr(payload, "data", payload)
    meta: WebhookMeta = {"timestamp": timestamp, "event": event_name}

    await events.dispatch(event_name, event_payload, meta)

    return WebhookResponse(message=f"{event_name} webhook received and verified")


@router.post("/order-created", response_model=WebhookResponse)
async def order_created(request: Request):
    """
    Receive **Order Created** webhook from Ghala.

    Triggered when:

        A new order is successfully placed by a customer.

    Payload includes:

        - Customer details (name, phone, email).
        - Order information (order ID, total amount, discounts).
        - Line items (products purchased with quantity and pricing).

    What this endpoint does:

        - Verifies the request signature for authenticity.
        - Dispatches an `order.created` event to your plugin system,
          enabling custom logic such as database persistence, analytics,
          or sending notifications.
        - Returns a confirmation response to Ghala.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.CREATE_ORDER_WEBHOOK_SECRET,
        event_name="order.created",
        model=OrderCreatedWebhook,
    )


@router.post("/order-updated", response_model=WebhookResponse)
async def order_updated(request: Request):
    """
    Receive **Order Updated** webhook from Ghala.

    Triggered when:

        An existing order’s details are modified, such as product quantities,
        applied discounts, or updated customer information.

    Payload includes:

        - Updated order metadata.
        - Modified product line items.
        - New totals (if applicable).

    What this endpoint does:

        - Validates and parses the update event.
        - Dispatches an `order.updated` event for custom handling,
          such as syncing with ERP/CRM systems or adjusting stock levels.
        - Responds with acknowledgment to Ghala.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.UPDATE_ORDER_WEBHOOK_SECRET,
        event_name="order.updated",
        model=OrderUpdatedWebhook,
    )


@router.post("/order-cancelled", response_model=WebhookResponse)
async def order_cancelled(request: Request):
    """
    Receive **Order Cancelled** webhook from Ghala.

    Triggered when:

        A customer or merchant cancels an existing order.

    Payload includes:

        - Cancelled order ID.
        - Customer information.
        - Reason for cancellation (if provided).

    What this endpoint does:

        - Ensures authenticity of the cancellation request.
        - Dispatches an `order.cancelled` event, enabling plugins to
          handle refunds, restock inventory, or update reporting systems.
        - Sends back acknowledgment to Ghala.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.CANCEL_ORDER_WEBHOOK_SECRET,
        event_name="order.cancelled",
        model=OrderCancelledWebhook,
    )


@router.post("/payment-successful", response_model=WebhookResponse)
async def payment_successful(request: Request):
    """
    Receive **Payment Successful** webhook from Ghala.

    Triggered when:

        A customer’s payment for an order is processed successfully.

    Payload includes:

        - Payment ID and method (e.g., card, mobile money).
        - Amount paid.
        - Associated order ID.

    What this endpoint does:

        - Confirms the payment authenticity.
        - Dispatches a `payment.successful` event, allowing plugins to
          activate subscriptions, update ledgers, or send confirmation messages.
        - Returns success acknowledgment to Ghala.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_SUCCESSFUL_WEBHOOK_SECRET,
        event_name="payment.successful",
        model=PaymentSuccessfulWebhook,
    )


@router.post("/payment-failed", response_model=WebhookResponse)
async def payment_failed(request: Request):
    """
    Receive **Payment Failed** webhook from Ghala.

    Triggered when:

        A customer’s payment attempt fails due to issues such as
        insufficient funds, expired card, or gateway error.

    Payload includes:

        - Failure reason.
        - Payment ID (if generated).
        - Associated order ID.

    What this endpoint does:

        - Validates and verifies the failure event.
        - Dispatches a `payment.failed` event to plugins, which can
          notify the customer, retry payments, or flag the order for review.
        - Responds with acknowledgment to Ghala.
    """
    return await handle_webhook(
        request,
        secret=settings.settings.PAYMENT_FAILED_WEBHOOK_SECRET,
        event_name="payment.failed",
        model=PaymentFailedWebhook,
    )
