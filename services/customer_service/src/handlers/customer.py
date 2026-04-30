import bcrypt
from uuid import UUID
from fastapi import APIRouter, Depends

from repository.repository_base_abc import CustomerRepositoryBase
from errors.exceptions import UnauthorizedException, NotFoundException
from auth_middleware.auth import create_access_token, get_curr_customer_id

from dtos.customer import (
    LoginCustomerDto, RegisterCustomerDto, UpdateCustomerDto,CustomerResponse, TokenResponse
)

router: APIRouter = APIRouter(tags=["customer"])

async def get_repository() -> CustomerRepositoryBase:
    ...

@router.post("/register")
async def register_customer(
    register_dto: RegisterCustomerDto,
    repo: CustomerRepositoryBase = Depends(get_repository)
) -> CustomerResponse:
    customer = await repo.register_customer(register_dto)
    return CustomerResponse.from_customer(customer)

@router.post("/login")
async def login_customer(
    login_dto: LoginCustomerDto,
    repo: CustomerRepositoryBase = Depends(get_repository)
) -> TokenResponse:
    customer = await repo.get_customer_by_username(login_dto.username)
    if not customer:
        raise UnauthorizedException("Invalid username or password!")

    if not bcrypt.checkpw(login_dto.password.encode("utf-8"), customer.password_hash.encode("utf-8")):
        raise UnauthorizedException("Invalid username or password!")

    access_token = create_access_token(customer.id, customer.username)
    return TokenResponse(access_token=access_token)

@router.get("/")
async def get_all_customers(
    repo: CustomerRepositoryBase = Depends(get_repository),
    _: UUID = Depends(get_curr_customer_id)
) -> list[CustomerResponse]:
    customers = await repo.get_all_customers()
    return [CustomerResponse.from_customer(customer) for customer in customers]

@router.get("/{customer_id}")
async def get_customer_by_id(
    customer_id: UUID,
    repo: CustomerRepositoryBase = Depends(get_repository),
    _: UUID = Depends(get_curr_customer_id)
) -> CustomerResponse:
    customer = await repo.get_customer_by_id(customer_id)
    if not customer:
        raise NotFoundException(f"Customer with id {customer_id} not found!")

    return CustomerResponse.from_customer(customer)

@router.patch("/{customer_id}")
async def update_customer(
    customer_id: UUID,
    update_dto: UpdateCustomerDto,
    repo: CustomerRepositoryBase = Depends(get_repository),
    curr_customer_id: UUID = Depends(get_curr_customer_id)
) -> CustomerResponse:
    if curr_customer_id != customer_id:
        raise UnauthorizedException("You can only update your own account!")

    updated_customer = await repo.update_customer(customer_id, update_dto)
    if not updated_customer:
        raise NotFoundException(f"Customer with id {customer_id} not found!")

    return CustomerResponse.from_customer(updated_customer)

@router.delete("/{customer_id}")
async def delete_customer(
    customer_id: UUID,
    repo: CustomerRepositoryBase = Depends(get_repository),
    curr_customer_id: UUID = Depends(get_curr_customer_id)
) -> bool:
    if curr_customer_id != customer_id:
        raise UnauthorizedException("You can only delete your own account!")

    deleted = await repo.delete_customer(customer_id)
    if not deleted:
        raise NotFoundException(f"Customer with id {customer_id} not found!")

    return True
