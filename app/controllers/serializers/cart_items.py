from pydantic import BaseModel, Field


class CartItems(BaseModel):
    product_id: int = Field(..., description="product_id")
    quantity: int = Field(..., description="Quantity")


class CartItemsUpdate(BaseModel):
    cart_id: int = Field(..., description="cart_id")
    product_id: int = Field(..., description="product_id")
    quantity: int = Field(..., description="Quantity")
