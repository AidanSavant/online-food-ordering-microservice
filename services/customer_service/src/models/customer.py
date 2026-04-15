from uuid import UUID
from pydantic import BaseModel, Field

from sqlalchemy import String
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column

class Customer(BaseModel):
    id: UUID
    username: str = Field(min_length=3, max_length=50)
    password_hash: str = Field(min_length=60, max_length=255)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

class BaseCustomerTable(DeclarativeBase):
    ...

class CustomerTable(BaseCustomerTable):
    __tablename__ = "customers"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
