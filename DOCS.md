A **Python FastAPI project** for handling Ghala webhooks, validating requests with HMAC signatures, and processing order and payment events. Built with **FastAPI**, **Pydantic**, and **async utilities** for high performance.

---

## Features

* Validate Ghala webhook requests using **HMAC SHA256 signatures**
* Protect against **replay attacks** with timestamp validation
* Structured Pydantic models for webhook payloads
* Generic webhook handler to simplify endpoint creation
* Plugin-based event handling system
* Easy environment configuration with `.env`
* Ready for adding new webhook events

---

## Installation

```bash
# Clone the repository
git clone https://github.com/erickweyunga/ghala-hooks
cd ghala-hooks

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
CREATE_ORDER_WEBHOOK_SECRET="your_create_order_secret"
UPDATE_ORDER_WEBHOOK_SECRET="your_update_order_secret"
CANCEL_ORDER_WEBHOOK_SECRET="your_cancel_order_secret"
PAYMENT_SUCCESSFUL_WEBHOOK_SECRET="your_payment_successful_secret"
PAYMENT_FAILED_WEBHOOK_SECRET="your_payment_failed_secret"

APP_NAME="Ghala Webhooks Service"
APP_VERSION="1.0.0"
ENVIRONMENT=development
REDOC_URL=/redoc
PLUGIN_PATH=app.plugins
```

> These secrets are provided by Ghala for webhook validation.

---

## Running the App

```bash
uvicorn app.main:app --reload
```

* Server will start at `http://127.0.0.1:8000`
* API documentation available at `http://127.0.0.1:8000/docs`
* ReDoc documentation at `http://127.0.0.1:8000/redoc`

### Expose with ngrok for webhook testing:

```bash
ngrok http 8000
```

---

## API Endpoints

| Method | Path                              | Description                    |
| ------ | --------------------------------- | ------------------------------ |
| POST   | /ghala/webhook/order-created      | Handle order creation webhook  |
| POST   | /ghala/webhook/order-updated      | Handle order update webhook    |
| POST   | /ghala/webhook/order-cancelled    | Handle order cancellation      |
| POST   | /ghala/webhook/payment-successful | Handle payment success webhook |
| POST   | /ghala/webhook/payment-failed     | Handle payment failed webhook  |

### Endpoint Details

**Order Created** (`/ghala/webhook/order-created`)
- Triggered when a new order is successfully placed
- Includes customer details, order information, and line items
- Dispatches `order.created` event to plugins

**Order Updated** (`/ghala/webhook/order-updated`)
- Triggered when order details are modified
- Includes updated order metadata and modified line items
- Dispatches `order.updated` event to plugins

**Order Cancelled** (`/ghala/webhook/order-cancelled`)
- Triggered when an order is cancelled
- Includes order ID, customer info, and cancellation reason
- Dispatches `order.cancelled` event to plugins

**Payment Successful** (`/ghala/webhook/payment-successful`)
- Triggered when payment is processed successfully
- Includes payment ID, method, amount, and order ID
- Dispatches `payment.successful` event to plugins

**Payment Failed** (`/ghala/webhook/payment-failed`)
- Triggered when payment attempt fails
- Includes failure reason, payment ID, and order ID
- Dispatches `payment.failed` event to plugins

---

## Schemas

All webhook payloads are validated using **Pydantic models**:

### Webhook Models
* `OrderCreatedWebhook`
* `OrderUpdatedWebhook`
* `OrderCancelledWebhook`
* `PaymentSuccessfulWebhook`
* `PaymentFailedWebhook`

### Shared Models
* `Customer` - Customer information
* `Product` - Product details and pricing
* `OrderData` - Complete order information
* `PaymentData` - Payment transaction details
* `WebhookResponse` - Standard response format

---

## Plugin System

The service supports a plugin-based event handling system. Create plugins in the `app/plugins` directory:

```python
# app/plugins/my_plugin.py
from app.webhooks.events import events
from app.schemas.webhooks import OrderData
from app.webhooks.events import WebhookMeta

PLUGIN_ACTIVE = True

@events.on("order.created")
async def handle_order_created(payload: OrderData, meta: WebhookMeta) -> None:
    """Handle new order creation"""
    print(f"New order created: {payload.order_id}")
    # Add your custom logic here

@events.on("payment.successful")
async def handle_payment_success(payload: OrderData, meta: WebhookMeta) -> None:
    """Handle successful payment"""
    print(f"Payment successful for order: {payload.order_id}")
    # Add your custom logic here

@events.on("*")
async def log_all_events(payload: OrderData, meta: WebhookMeta) -> None:
    """Log all webhook events"""
    event_name = meta.get("event", "unknown")
    print(f"[{event_name}] Order ID: {payload.order_id}")
```

### Available Events
* `order.created`
* `order.updated`
* `order.cancelled`
* `payment.successful`
* `payment.failed`
* `*` (wildcard for all events)

---

## Security Features

### HMAC Signature Verification
Each webhook request is validated using HMAC SHA256 signatures to ensure authenticity.

### Timestamp Validation
Protects against replay attacks by validating request timestamps.

### Request Validation
All payloads are validated using Pydantic models for type safety and data integrity.

---

## Testing Webhooks

1. **Expose your server with ngrok**:
   ```bash
   ngrok http 8000
   ```

2. **Configure webhook URLs in Ghala dashboard**:
   - Use the ngrok public URL + endpoint paths
   - Example: `https://abc123.ngrok.io/ghala/webhook/order-created`

3. **Test webhook delivery**:
   - Create test orders in Ghala
   - Monitor logs for incoming webhooks
   - Verify plugin execution

4. **Use FastAPI docs for manual testing**:
   - Visit `http://127.0.0.1:8000/docs`
   - Test endpoints directly from the interface

---

## Project Structure

```
app/
├── main.py                 # FastAPI app entry point
├── settings.py             # Environment configuration
├── docs.py                 # Documentation loader
├── routes/
│   └── webhooks.py         # Webhook routes & handlers
├── webhooks/
│   ├── __init__.py
│   ├── utils.py            # Signature & timestamp verification
│   └── events.py           # Event system for plugins
├── schemas/
│   └── webhooks.py         # Pydantic models
├── plugins/                # Plugin directory
│   └── example_plugin.py   # Example event handlers
requirements.txt
DOCS.md                     # This documentation
.env                        # Environment variables
```

---

## Development

### Creating Plugins

1. Create Python file in `app/plugins/`
2. Import events system: `from app.webhooks.events import events`
3. Use `@events.on("event.name")` decorator
4. Set `PLUGIN_ACTIVE = True` to enable the plugin

---

## Next Steps

* Configure `.env` with your webhook secrets from Ghala
* Register webhook endpoints in your Ghala dashboard
* Create custom plugins in `app/plugins/` for your business logic
* Test webhook delivery using ngrok and the Ghala platform
* Monitor logs and verify successful event processing

---

For more information, visit the [Ghala Documentation](https://ghala.tz/for-developers)
