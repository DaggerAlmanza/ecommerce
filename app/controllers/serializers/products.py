from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional


class Products(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = Field(
        None,
        description="Description"
    )
    price: Decimal = Field(..., description="Price")
    stock_quantity: Optional[int] = Field(
        0,
        description="Stock quantity"
    )
    image_url: Optional[str] = Field(
        None,
        description="Image"
    )


class ProductsUpdate(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = Field(
        None,
        description="Description"
    )
    price: Decimal = Field(..., description="Price")
    stock_quantity: Optional[int] = Field(
        0,
        description="Stock quantity"
    )
    image_url: Optional[str] = Field(
        None,
        description="Image"
    )
    creator_id: int = Field(..., description="Creator id")
