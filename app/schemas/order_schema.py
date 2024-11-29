from enum import Enum

from pydantic import BaseModel, Field, validator


class CryptoTypes(str, Enum):
    ABAN = 'ABAN'
    BITCOIN = 'BITCOIN'
    OTHER = 'OTHER'


class OrderCreate(BaseModel):
    user_id: str = Field(default="39", pattern=r"^\d+$", description="User ID must be a numeric string.")
    crypto_name: CryptoTypes = Field(default="ABAN", description="Type of cryptocurrency.")
    amount: str = Field(default="1", pattern=r"^\d+(\.\d{1,2})?$",
                        description="Amount must be a valid number with up to 2 decimal places.")
    price_per_unit: str = Field(default="4", pattern=r"^\d+(\.\d{1,2})?$",
                                description="Price per unit must be a valid number with up to 2 decimal places.")

    @validator("amount", "price_per_unit")
    def validate_positive_values(cls, value):
        if float(value) <= 0:
            raise ValueError(f"{value} must be a positive number.")
        return value

    @validator("user_id")
    def validate_user_id_length(cls, value):
        if len(value) > 10:
            raise ValueError("User ID must not exceed 10 characters.")
        return value


class OrderResponse(BaseModel):
    order_id: int
    status: str

    class Config:
        orm_mode = True
