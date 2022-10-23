from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

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

inventory = []

#######################################

@app.get("/inventory/all")
async def list_inventory():
    return inventory

@app.get("/product/all")
async def list_products():
    return products

@app.post("/product/transaction")
async def product_transaction(product_id: int, qty: int):
    if (product_id in products):
        product = dict( products[product_id] )

        new_qty = product['quantity'] + qty
        product['quantity'] = new_qty

        products[product_id] = jsonable_encoder(product)

        inventory.append({"product_id" : product_id, "quantity" : qty}) 
        return product
    else:
        raise HTTPException(status_code=404, detail="product does not exist")

@app.post("/product")
async def create_product(product: Product):
    if (product.id in products):
        raise HTTPException(status_code=404, detail="product already exists")
    else:
        products[product.id] = product
        return product

@app.put("/product")
async def update_product(Product):
    return {"message": "Hello World"}

@app.get("/product/{product_id}")
async def get_product(product_id: int):
    if (product_id in products):
        return products[product_id]
    else :
        raise HTTPException(status_code=404, detail="product does not exist")

@app.delete("/product")
async def delete_product(product_id: int):
    if (product_id in products) :
        del products[product_id]
    else :
        raise HTTPException(status_code=404, detail="product does not exist")

@app.get("/")
async def root():
    return {"message": "Hello World"}