from pydantic import BaseModel, validator
from typing import List
import re

class Item(BaseModel):
    title: str
    unit_price: float
    quantity: int
    currency_id: str = "ARS"

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
    success: str = 'https://tienda-wep-creaciones-vuela.netlify.app/'  # URL del home
    failure: str = 'https://tienda-wep-creaciones-vuela.netlify.app/'  # URL del home
    pending: str = 'https://tienda-wep-creaciones-vuela.netlify.app/'  # URL del home

    @validator("success", "failure", "pending", pre=True)
    def validate_url(cls, value):
        if value and not re.match(r'http(s)?://', value):
            raise ValueError(f"{value} no es una URL válida")
        return value

class DataPreference(BaseModel):
    items: List[Item]
    back_urls: BackUrl  # No es opcional, siempre se enviará
    payer_email: EmailStr = "neyenfrandino1@gmail.com"  # Campo añadido para el correo del comprador
    auto_return: str = "approved"  # Cambiado a str con valor por defecto

    @validator("auto_return")
    def validate_auto_return(cls, value):
        if value not in ["approved", "all"]:
            raise ValueError("auto_return debe ser 'approved' o 'all'")
        return value