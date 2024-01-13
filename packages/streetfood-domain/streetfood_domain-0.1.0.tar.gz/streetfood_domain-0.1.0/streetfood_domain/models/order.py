from __future__ import annotations
from pydantic import BaseModel


class Order(BaseModel):
    id: str
    cart: Cart
    contact: Contact
    is_ready: bool
    done: bool


class Contact(BaseModel):
    name: str
    phone: str


class Cart(BaseModel):
    id: str
    lines: list[Line]


class Line(BaseModel):
    id: str
    product: Product
    quantity: int


class Product(BaseModel):
    id: str
    price: float

