from fastapi import FastAPI
from app.routes import webhooks

app = FastAPI(title="Ghala Webhooks API")

app.include_router(webhooks.router, prefix="/ghala/webhook", tags=["Webhooks"])
