import bcrypt
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.customer import Customer, CustomerTable
from dtos.customer import RegisterCustomerDto, UpdateCustomerDto
from errors.exceptions import (
    CustomerException,
    ConflictException,
    DatabaseException
)
from repository.repository_base_abc import CustomerRepositoryBase

class PostgresCustomerRepository(CustomerRepositoryBase):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_domain_model(customer_table: CustomerTable) -> Customer:
        return Customer(
            id=customer_table.id,
            username=customer_table.username,
            password_hash=customer_table.password_hash,
            first_name=customer_table.first_name,
            last_name=customer_table.last_name
        )
    
    async def get_all_customers(self) -> list[Customer]:
        try:
            res = await self.session.execute(select(CustomerTable))
            return [self._to_domain_model(row) for row in res.scalars().all()]

        except Exception as e:
            raise DatabaseException(f"Failed getting all customers! Reason: {str(e)}")

    async def get_customer_by_id(self, customer_id: UUID) -> Customer | None:
        try:
            res = await self.session.execute(
                select(CustomerTable)
                .where(CustomerTable.id == customer_id)
            )
            customer_table = res.scalar_one_or_none()

            return self._to_domain_model(customer_table) if customer_table else None
        except Exception as e:
            raise DatabaseException(f"Failed getting customer by id! Reason: {str(e)}")
        
    async def get_customer_by_username(self, username: str) -> Customer | None:
        try:
            res = await self.session.execute(
                select(CustomerTable)
                .where(CustomerTable.username == username)
            )
            customer_table = res.scalar_one_or_none()

            return self._to_domain_model(customer_table) if customer_table else None
        except Exception as e:
            raise DatabaseException(f"Failed getting customer by username! Reason: {str(e)}")
        
    async def register_customer(self, customer: RegisterCustomerDto) -> Customer:
        try:
            password_hash = bcrypt.hashpw(customer.password.encode("utf-8"), bcrypt.gensalt())
            new_customer = CustomerTable(
                id=uuid4(),
                username=customer.username,
                password_hash=password_hash.decode("utf-8"),
                first_name=customer.first_name,
                last_name=customer.last_name
            )

            self.session.add(new_customer)
            await self.session.commit()
            await self.session.refresh(new_customer)

            return self._to_domain_model(new_customer)
        except IntegrityError:
            await self.session.rollback()
            raise ConflictException(f"Username '{customer.username}' already exists!")
        
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Failed registering customer! Reason: {str(e)}")

    async def update_customer(self, customer_id: UUID, update_dto: UpdateCustomerDto) -> Customer | None:
        try:
            res = await self.session.execute(
                select(CustomerTable)
                .where(CustomerTable.id == customer_id)
            )

            customer_table = res.scalar_one_or_none()
            if not customer_table:
                return None
            
            if update_dto.username is not None:
                customer_table.username = update_dto.username
            
            if update_dto.first_name is not None:
                customer_table.first_name = update_dto.first_name
            
            if update_dto.last_name is not None:
                customer_table.last_name = update_dto.last_name
            
            if update_dto.new_password is not None:
                if update_dto.curr_password is None:
                    raise CustomerException("Current password is required to set a new password!")

                if not bcrypt.checkpw(update_dto.curr_password.encode("utf-8"), customer_table.password_hash.encode("utf-8")):
                    raise CustomerException("Current password is incorrect!")
                
                customer_table.password_hash = bcrypt.hashpw(update_dto.new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

            await self.session.commit()
            await self.session.refresh(customer_table)

            return self._to_domain_model(customer_table)

        except IntegrityError:
            await self.session.rollback()
            raise ConflictException(f"Username '{update_dto.username}' already exists!")
        
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Failed updating customer! Reason: {str(e)}")

    async def delete_customer(self, customer_id: UUID) -> bool:
        try:
            res = await self.session.execute(
                select(CustomerTable)
                .where(CustomerTable.id == customer_id)
            )

            customer_table = res.scalar_one_or_none()
            if not customer_table:
                return False
            
            await self.session.delete(customer_table)
            await self.session.commit()

            return True
        except Exception as e:
            await self.session.rollback()
            raise DatabaseException(f"Failed deleting customer! Reason: {str(e)}")
