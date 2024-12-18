from pydantic import BaseModel, validator
from typing import List
import re

class Item(BaseModel):
    title: str
    unit_price: float
    quantity: int

    @validator("unit_price")
    def validate_unit_price(cls, value):
        if value <= 0:
            raise ValueError("unit_price must be greater than 0")
        return value

    @validator("quantity")
    def validate_quantity(cls, value):
        if value <= 0:
            raise ValueError("quantity must be greater than 0")
        return value

class BackUrl(BaseModel):
    success: str = 'http://localhost:3000/'
    failure: str = 'http://localhost:3000/'
    pending: str = 'http://localhost:3000/'  # Ahora está presente por defecto

    @validator("success", "failure", "pending", pre=True)
    def validate_url(cls, value):
        if value and not re.match(r'http(s)?://', value):
            raise ValueError(f"{value} is not a valid URL")
        return value

class DataPreference(BaseModel):
    items: List[Item]
    back_urls: BackUrl  # No es opcional, siempre se enviará
    auto_return: str = "approved"  # Cambiado a str con valor por defecto

    @validator("auto_return")
    def validate_auto_return(cls, value):
        if value not in ["approved", "all"]:
            raise ValueError("auto_return must be either 'approved' or 'all'")
        return value
