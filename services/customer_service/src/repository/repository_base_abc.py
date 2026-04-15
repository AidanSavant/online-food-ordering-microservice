from uuid import UUID
from abc import ABC, abstractmethod

from models.customer import Customer
from dtos.customer import RegisterCustomerDto, UpdateCustomerDto

class CustomerRepositoryBase(ABC):
    @abstractmethod
    async def get_all_customers(self) -> list[Customer]:
        ...

    @abstractmethod
    async def get_customer_by_id(self, customer_id: UUID) -> Customer | None:
        ...

    @abstractmethod
    async def get_customer_by_username(self, username: str) -> Customer | None:
        ...

    @abstractmethod
    async def register_customer(self, customer: RegisterCustomerDto) -> Customer:
        ...

    @abstractmethod
    async def update_customer(self, customer_id: UUID, update_dto: UpdateCustomerDto) -> Customer | None:
        ...

    @abstractmethod
    async def delete_customer(self, customer_id: UUID) -> bool:
        ...
