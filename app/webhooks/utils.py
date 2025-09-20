import time
import hmac
import hashlib
import base64
from fastapi import Request, HTTPException


def verify_timestamp(timestamp: str, max_age_seconds: int = 300):
    """
    Check if the timestamp is within the allowed time window (default 5 minutes).
    Supports floating-point timestamps.
    """
    try:
        ts = float(timestamp)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp")

    now = time.time()
    if abs(now - ts) > max_age_seconds:
        raise HTTPException(status_code=400, detail="Stale timestamp")


def verify_signature(secret: str, timestamp: str, body: bytes, signature: str):
    """
    Verify the HMAC SHA256 signature from Ghala.
    Raises HTTPException if signature is invalid.
    """
    signed_content = f"{timestamp}.{body.decode('utf-8')}"
    secret_bytes = secret.encode("utf-8")
    computed_hmac = hmac.new(secret_bytes, signed_content.encode("utf-8"), hashlib.sha256).digest()
    expected_signature = base64.b64encode(computed_hmac).decode()

    if not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=400, detail="Invalid signature")


async def extract_webhook_data(request: Request):
    """
    Extract headers and body from the request, and normalize header names.
    Returns: (timestamp, signature, body)
    """
    headers = {k.lower(): v for k, v in request.headers.items()}
    body = await request.body()

    timestamp = headers.get("x-ghala-timestamp") or headers.get("webhook-timestamp")
    signature = headers.get("x-ghala-signature")

    if not timestamp or not signature:
        raise HTTPException(status_code=400, detail="Missing required headers")

    return timestamp, signature, body
