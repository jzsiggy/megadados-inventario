from typing import List, Union

from pydantic import BaseModel

class Product(BaseModel):
    id: Union [int, None] = None
    name: Union [str, None] = None
    description: Union [str, None] = None
    price:  Union [float, None] = None
    quantity:  Union [int, None] = None
    removed: Union [bool, None] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123,
                "name": "Foo",
                "description": "A very nice product",
                "price": 35.4,
                "quantity": 456,
                "removed": 0
            }
        }

class Inventory(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_id": 123,
                "quantity": -4
            }
        }