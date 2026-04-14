from uuid import UUID
from fastapi import APIRouter, Depends

from models.cart import Cart, CartItem, ItemQuantity
from repository.cart_repo_base import CartRepositoryABC
from errors.exceptions import NotFoundException, CartBaseException

router: APIRouter = APIRouter()

async def get_repository() -> CartRepositoryABC:
    ...

async def _get_cart(
    cart_id: UUID,
    repo: CartRepositoryABC
) -> Cart:
    cart = await repo.get_cart(cart_id)
    if not cart:
        raise NotFoundException(f"Cart with id {cart_id} not found")
    
    return cart

@router.get("/{user_id}")
async def get_cart_handler(
    user_id: UUID,
    repo: CartRepositoryABC = Depends(get_repository)
) -> Cart:
    return await _get_cart(user_id, repo)

@router.post("/{user_id}/items")
async def add_item_handler(
    user_id: UUID,
    item: CartItem,
    repo: CartRepositoryABC = Depends(get_repository)
) -> Cart:
    return await repo.add_item(user_id, item)

@router.patch("/{user_id}/items/{item_id}")
async def update_item_quantity_handler(
    user_id: UUID,
    item_id: UUID,
    quantity: ItemQuantity,
    repo: CartRepositoryABC = Depends(get_repository)
) -> Cart:
    return await repo.update_item_quantity(user_id, item_id, quantity)

@router.delete("/{user_id}/items/{item_id}")
async def remove_item_handler(
    user_id: UUID,
    item_id: UUID,
    repo: CartRepositoryABC = Depends(get_repository)
) -> Cart:
    return await repo.remove_item(user_id, item_id)

@router.delete("/{user_id}/items")
async def clear_cart_handler(
    user_id: UUID,
    repo: CartRepositoryABC = Depends(get_repository)
) -> None:
    return await repo.clear_cart(user_id)

@router.delete("/{user_id}")
async def delete_cart_handler(
    user_id: UUID,
    repo: CartRepositoryABC = Depends(get_repository)
) -> bool:
    return await repo.delete_cart(user_id)
