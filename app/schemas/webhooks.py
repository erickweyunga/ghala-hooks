from typing import List, Optional
from pydantic import BaseModel, Field


class Customer(BaseModel):
    name: str
    phone: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

    class Config:
        extra = "ignore"


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    unique_id: Optional[str] = None
    discount_amount: Optional[float] = Field(default=0.0)
    additional_cost: Optional[float] = Field(default=0.0)
    additional_cost_description: Optional[str] = None
    quantity: float

    class Config:
        extra = "ignore"


class OrderData(BaseModel):
    customer: Customer
    order_id: int
    total: float
    discount_total: Optional[float] = Field(default=0.0)
    promo_discount_amount: Optional[float] = Field(default=0.0)
    products: List[Product]

    class Config:
        extra = "ignore"


class OrderCreatedWebhook(BaseModel):
    event: str
    data: OrderData

    class Config:
        extra = "ignore"


class OrderUpdatedWebhook(BaseModel):
    event: str
    data: OrderData

    class Config:
        extra = "ignore"


class OrderCancelledWebhook(BaseModel):
    event: str
    timestamp: Optional[float] = None
    data: OrderData

    class Config:
        extra = "ignore"


class PaymentData(BaseModel):
    order_id: int
    amount: float
    currency: str
    payment_id: str
    status: str
    customer: Customer

    class Config:
        extra = "ignore"


class PaymentSuccessfulWebhook(BaseModel):
    event: str
    timestamp: Optional[float] = None
    data: PaymentData

    class Config:
        extra = "ignore"


class PaymentFailedWebhook(BaseModel):
    event: str
    timestamp: Optional[float] = None
    data: PaymentData

    class Config:
        extra = "ignore"
