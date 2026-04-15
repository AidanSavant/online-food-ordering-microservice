from uuid import UUID
from pydantic import BaseModel, Field, model_validator

from models.customer import Customer

class RegisterCustomerDto(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=50)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)

class LoginCustomerDto(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=50)

class UpdateCustomerDto(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    curr_password: str | None = Field(default=None, min_length=6, max_length=50)
    new_password: str | None = Field(default=None, min_length=6, max_length=50)
    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name:  str | None = Field(default=None, min_length=1, max_length=50)

    @model_validator(mode="after")
    def validate_passwords(self) -> "UpdateCustomerDto":
        if self.new_password and not self.curr_password:
            raise ValueError("Current password is required to change password! ")
        
        if self.curr_password and not self.new_password:
            raise ValueError("New password is required to change password!")

        return self

class CustomerResponse(BaseModel):
    id: UUID
    username: str
    first_name: str
    last_name: str

    @classmethod
    def from_customer(cls, customer: Customer) -> "CustomerResponse":
        return cls(
            id=customer.id,
            username=customer.username,
            first_name=customer.first_name,
            last_name=customer.last_name
        )

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
