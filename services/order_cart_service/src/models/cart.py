from uuid import UUID
from pydantic import BaseModel, Field

QUANTITY_FIELD = Field(ge=1)

class ItemQuantity(BaseModel):
    quantity: int = QUANTITY_FIELD

class CartItem(BaseModel):
    item_id: UUID
    restaurant_id: UUID

    name: str = Field(min_length=1, max_length=255)
    price: float = Field(ge=0.50)
    quantity: int = QUANTITY_FIELD

class Cart(BaseModel):
    user_id: UUID
    items: dict[str, CartItem] = {}
