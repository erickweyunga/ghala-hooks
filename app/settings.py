from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CREATE_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for create order webhook", init=False)
    CANCEL_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for cancel order webhook", init=False)
    UPDATE_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for update order webhook", init=False)
    PAYMENT_SUCCESSFUL_WEBHOOK_SECRET: str = Field(..., description="Secret for payment successful webhook", init=False)
    PAYMENT_FAILED_WEBHOOK_SECRET: str = Field(..., description="Secret for payment failed webhook", init=False)

    APP_NAME: str = Field("Ghala Webhooks API", description="Application name", init=False)
    APP_DESCRIPTION: str = Field(
        "A FastAPI service to handle Ghala webhooks, dispatch events to plugins, "
        "and manage order/payment notifications.", description="Application description", init=False
    )
    APP_VERSION: str = Field("1.0.0", description="Application version", init=False)
    ENVIRONMENT: str = Field("development", description="Application environment (development|staging|production)", init=False)

    REDOC_URL: str = Field("/redoc", description="Redoc URL", init=False)

    PLUGIN_PATH: str = Field("app.plugins", description="Python package path to load plugins from", init=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
