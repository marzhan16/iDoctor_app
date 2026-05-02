from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime
from uuid import uuid4


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class OrderCreate(BaseModel):
    parkingId: str
    userId: str
    duration: int  # in hours
    startTime: datetime


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    parkingId: str
    userId: str
    duration: int
    startTime: datetime
    endTime: datetime
    status: OrderStatus = OrderStatus.PENDING
    createdAt: datetime = Field(default_factory=datetime.now)
    totalPrice: float = 0.0
    paymentId: Optional[str] = None


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    paymentId: Optional[str] = None