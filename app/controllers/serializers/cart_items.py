from pydantic import BaseModel, Field


class CartItems(BaseModel):
    product_id: int = Field(..., description="product_id")
    quantity: int = Field(..., description="Quantity")
