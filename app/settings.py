from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CREATE_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for create order webhook", init=False)
    CANCEL_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for cancel order webhook", init=False)
    UPDATE_ORDER_WEBHOOK_SECRET: str = Field(..., description="Secret for update order webhook", init=False)
    PAYMENT_SUCCESSFUL_WEBHOOK_SECRET: str = Field(..., description="Secret for payment successful webhook", init=False)
    PAYMENT_FAILED_WEBHOOK_SECRET: str = Field(..., description="Secret for payment failed webhook", init=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
