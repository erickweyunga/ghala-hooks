# Ghala Webhooks Service

A **Python FastAPI project** for handling Ghala webhooks, validating requests with HMAC signatures, and processing order and payment events. Built with **FastAPI**, **Pydantic**, and **async utilities** for high performance.

---

## **Table of Contents**

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Running the App](#running-the-app)
* [API Endpoints](#api-endpoints)
* [Schemas](#schemas)
* [Testing Webhooks](#testing-webhooks)
* [Project Structure](#project-structure)
* [License](#license)

---

## **Features**

* Validate Ghala webhook requests using **HMAC SHA256 signatures**
* Protect against **replay attacks** with timestamp validation
* Structured Pydantic models for webhook payloads
* Generic webhook handler to simplify endpoint creation
* Ready for adding new webhook events
* Easy environment configuration with `.env`
* Supports plugin-based event handling

---

## **Requirements**

* Python 3.11+
* [FastAPI](https://fastapi.tiangolo.com/)
* [Uvicorn](https://www.uvicorn.org/)
* [Pydantic](https://docs.pydantic.dev/)

---

## **Installation**

```bash
# Clone the repository
git clone https://github.com/erickweyunga/ghala-hooks
cd python-webhooks

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

---

## **Environment Variables**

Create a `.env` file in the project root:

```env
CREATE_ORDER_WEBHOOK_SECRET="your_create_order_secret"
UPDATE_ORDER_WEBHOOK_SECRET="your_update_order_secret"
CANCEL_ORDER_WEBHOOK_SECRET="your_cancel_order_secret"
PAYMENT_SUCCESSFUL_WEBHOOK_SECRET="your_payment_successful_secret"
PAYMENT_FAILED_WEBHOOK_SECRET="your_payment_failed_secret"
```

> These secrets are provided by Ghala for webhook validation.

---

## **Running the App**

```bash
uvicorn app.main:app --reload
```

* Server will start at `http://127.0.0.1:8000`
* Use **ngrok** to expose local server for webhook testing:

```bash
ngrok http 8000
```

---

## **API Endpoints**

| Method | Path                              | Description                    |
| ------ | --------------------------------- | ------------------------------ |
| POST   | /ghala/webhook/order-created      | Handle order creation webhook  |
| POST   | /ghala/webhook/order-updated      | Handle order update webhook    |
| POST   | /ghala/webhook/order-cancelled    | Handle order cancellation      |
| POST   | /ghala/webhook/payment-successful | Handle payment success webhook |
| POST   | /ghala/webhook/payment-failed     | Handle payment failed webhook  |

---

## **Schemas**

All webhook payloads are validated using **Pydantic models**:

* `OrderCreatedWebhook`
* `OrderUpdatedWebhook`
* `OrderCancelledWebhook`
* `PaymentSuccessfulWebhook`
* `PaymentFailedWebhook`

Shared models include:

* `Customer`
* `Product`
* `OrderData`
* `PaymentData`

---

## **Testing Webhooks**

1. Expose your server with **ngrok**:

   ```bash
   ngrok http 8000
   ```
2. Use the public URL in your Ghala webhook settings.
3. Send test payloads and verify logs.

---

## **Project Structure**

```
app/
├─ main.py                 # FastAPI app entry point
├─routes/
│  └─ webhooks.py          # Webhook routes & generic handler
├─webhooks/
│  └─ utils.py             # Signature & timestamp verification
├─schemas/
│  └─ webhooks.py          # Pydantic models
├─plugins/                 # Optional event plugins
├─settings.py              # Environment configuration
requirements.txt
```
