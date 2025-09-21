from fastapi import FastAPI
from app.routes import webhooks
from app.settings import settings
from app.webhooks.loader import load_plugins

load_plugins(settings.PLUGIN_PATH)

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=None,
    redoc_url=settings.REDOC_URL,
    openapi_url="/openapi.json"
)

app.include_router(webhooks.router)
