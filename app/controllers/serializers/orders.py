from enum import Enum
from pydantic import BaseModel, Field


class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Orders(BaseModel):
    status: OrderStatus = Field(..., description="Status")
