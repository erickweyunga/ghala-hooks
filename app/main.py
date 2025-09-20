from fastapi import FastAPI
from app.routes import webhooks
import pkgutil
import importlib
import app.plugins

for loader, module_name, is_pkg in pkgutil.iter_modules(app.plugins.__path__):
    importlib.import_module(f"app.plugins.{module_name}")

app = FastAPI(title="Ghala Webhooks API")

app.include_router(webhooks.router, prefix="/ghala/webhook", tags=["Webhooks"])
