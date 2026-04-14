from uuid import UUID

import redis.asyncio as redis

from models.cart import Cart, CartItem, ItemQuantity
from repository.cart_repo_base import CartRepositoryABC
from errors.exceptions import NotFoundException, DatabaseException

CART_TTL: int = 60 * 60 * 24
CART_KEY_PREFIX: str = "cart:"

class RedisCartRepository(CartRepositoryABC):
    def __init__(self, client: redis.Redis):
        self.client = client

    def _cart_key(self, user_id: UUID) -> str:
        return f"{CART_KEY_PREFIX}{user_id}"
    
    async def _create_cart(self, user_id: UUID) -> Cart:
        cart = await self.get_cart(user_id)
        if cart is None:
            cart = Cart(user_id=user_id)

        return cart
    
    async def _save_cart(self, cart: Cart) -> Cart:
        try:
            key = self._cart_key(cart.user_id)
            await self.client.setex(
                key,
                CART_TTL,
                cart.model_dump_json()
            )

            return cart
        except Exception as e:
            raise DatabaseException(f"Failed to save cart to Redis! Reason: {str(e)}")

    async def get_cart(self, user_id: UUID) -> Cart | None:
        try:
            key = self._cart_key(user_id)
            cart_json = await self.client.get(key)

            if cart_json is None:
                return None

            return Cart.model_validate_json(cart_json)
        except Exception as e:
            raise DatabaseException(f"Failed to retrieve cart from Redis! Reason: {str(e)}")

    async def add_item(self, user_id: UUID, item: CartItem) -> Cart:
        cart = await self._create_cart(user_id)
        cart.items[str(item.item_id)] = item

        return await self._save_cart(cart)
    
    async def update_item_quantity(self, user_id: UUID, item_id: UUID, quantity: ItemQuantity) -> Cart:
        cart = await self.get_cart(user_id)
        if cart is None:
            raise NotFoundException("Cart not found for user!")

        item_key = str(item_id)
        if item_key not in cart.items:
            raise NotFoundException("Item not found in cart!")

        cart.items[item_key].quantity = quantity.quantity
        return await self._save_cart(cart)
    
    async def remove_item(self, user_id: UUID, item_id: UUID) -> Cart:
        cart = await self.get_cart(user_id)
        if cart is None:
            raise NotFoundException(f"Cart not found for user {user_id}!")

        item_key = str(item_id)
        if item_key not in cart.items:
            raise NotFoundException(f"Item ID {item_id} not found in cart for user {user_id}!")

        del cart.items[item_key]
        return await self._save_cart(cart)

    async def clear_cart(self, user_id: UUID) -> None:
        cart = await self.get_cart(user_id)
        if cart is None:
            raise NotFoundException(f"Cart not found for user {user_id}!")
        
        cart.items.clear()
        await self._save_cart(cart)

    async def delete_cart(self, user_id: UUID) -> bool:
        try:
            key = self._cart_key(user_id)
            result = await self.client.delete(key)

            return result > 0
        except Exception as e:
            raise DatabaseException(f"Failed to delete cart from Redis! Reason: {str(e)}")
