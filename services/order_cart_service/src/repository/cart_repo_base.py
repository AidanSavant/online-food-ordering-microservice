from uuid import UUID
from abc import ABC, abstractmethod

from models.cart import Cart, CartItem, ItemQuantity

class CartRepositoryABC(ABC):
    @abstractmethod
    async def get_cart(self, user_id: UUID) -> Cart | None:
        ...

    @abstractmethod
    async def add_item(self, user_id: UUID, item: CartItem) -> Cart:
        ...

    @abstractmethod
    async def update_item_quantity(self, user_id: UUID, item_id: UUID, quantity: ItemQuantity) -> Cart:
        ...

    @abstractmethod
    async def remove_item(self, user_id: UUID, item_id: UUID) -> Cart:
        ...

    @abstractmethod
    async def clear_cart(self, user_id: UUID) -> None:
        ...

    @abstractmethod
    async def delete_cart(self, user_id: UUID) -> bool:
        ...
