from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#######################################

app = FastAPI()

#######################################

class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "id": 123,
                "name": "Foo",
                "description": "A very nice product",
                "price": 35.4,
                "quantity": 456,
            }
        }

class Inventory(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "product_id": 123,
                "quantity": -4
            }
        }

#######################################

products = {}

inventory = {}

#######################################

@app.post("/product/transaction")
async def product_transaction(product_id: int, qty: int):
    return {"message": "Hello World"}

@app.post("/product")
async def create_product(product: Product):
    # Criar um produto
    if (product.id in products) :
        raise HTTPException(status_code=404, detail="product already exists")
    else :
        products[product.id] = product
        return product

@app.put("/product")
async def update_product(Product):
    return {"message": "Hello World"}

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    if (product_id in products) :
        return products[product_id]
    else :
        raise HTTPException(status_code=404, detail="product does not exist")

@app.get("/product/all")
async def list_products():
    return {"message": "Hello World"}

@app.delete("/product")
async def delete_product():
    return {"message": "Hello World"}

@app.get("/")
async def root():
    return {"message": "Hello World"}