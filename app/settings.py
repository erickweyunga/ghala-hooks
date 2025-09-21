from pydantic import Field
from pydantic_settings import BaseSettings
from app.docs import get_app_description


class Settings(BaseSettings):
    CREATE_ORDER_WEBHOOK_SECRET: str = Field(
        ...,
        description="Secret for create order webhook. "
                    "Set this in your `.env` file as CREATE_ORDER_WEBHOOK_SECRET=your_secret",
                    init=False
    )
    CANCEL_ORDER_WEBHOOK_SECRET: str = Field(
        ...,
        description="Secret for cancel order webhook. "
                    "Add CANCEL_ORDER_WEBHOOK_SECRET=your_secret in `.env`",
                    init=False
    )
    UPDATE_ORDER_WEBHOOK_SECRET: str = Field(
        ...,
        description="Secret for update order webhook. "
                    "Define UPDATE_ORDER_WEBHOOK_SECRET=your_secret inside `.env`",
                    init=False
    )
    PAYMENT_SUCCESSFUL_WEBHOOK_SECRET: str = Field(
        ...,
        description="Secret for payment successful webhook. "
                    "Place PAYMENT_SUCCESSFUL_WEBHOOK_SECRET=your_secret in `.env`",
                    init=False
    )
    PAYMENT_FAILED_WEBHOOK_SECRET: str = Field(
        ...,
        description="Secret for payment failed webhook. "
                    "Use PAYMENT_FAILED_WEBHOOK_SECRET=your_secret in `.env`",
                    init=False
    )
    APP_NAME: str = Field(
        "Ghala Webhooks Service",
        description="Application name.",
        init=False
    )
    APP_DESCRIPTION: str = Field(
        default_factory=get_app_description,
        description="Application description loaded from DOCS.md file",
        init=False
    )
    APP_VERSION: str = Field(
        "1.0.0",
        description="Application version.",
        init=False
    )
    ENVIRONMENT: str = Field(
        "development",
        description="Application environment (development|staging|production).",
        init=False
    )
    REDOC_URL: str = Field(
        "/redoc",
        description="Path for ReDoc documentation.",
        init=False
    )
    PLUGIN_PATH: str = Field(
        "app.plugins",
        description="Python package path to load plugins from.",
        init=False
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
