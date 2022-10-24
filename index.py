from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

#######################################

app = FastAPI()

#######################################

# Declarando a base do modelo de produto e um exemplo dele
class Product(BaseModel):
    id: Union [int, None] = None
    name: Union [str, None] = None
    description: Union [str, None] = None
    price:  Union [float, None] = None
    quantity:  Union [int, None] = None

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

# Declarando a base do modelo de estoque e um exemplo dele
class Inventory(BaseModel):
    product_id: int
    quantity: int

    class Config:
        schema_extra = {
            "example": {
                "product_id": 123,
                "quantity": -4
            }
        }

###################################### INICIALIZANDO PRODUTO E ESTOQUE ######################################

products = {}

inventory = []

###################################### INPLEMENTAÇÃO DO CRUD ######################################



# GET -> mostra o estoque com os produtos
@app.get("/inventory/all")
async def list_inventory():
    return inventory

# GET -> todos os produtos do estoque
@app.get("/product/all")
async def list_products():
    return products

#POST -> movimentação dos produtos dentro do estoque; adicionar produtos etc
@app.post("/product/transaction")
async def product_transaction(movement: Inventory):
    product_id = movement.product_id
    qty = movement.quantity

    if (product_id in products):
        product = dict( products[product_id] )

        new_qty = product['quantity'] + qty
        product['quantity'] = new_qty

        products[product_id] = jsonable_encoder(product)

        inventory.append({"product_id" : product_id, "quantity" : qty}) 
        return product
    else:
        raise HTTPException(status_code=404, detail="product does not exist")

# POST -> cria um produto qualquer
@app.post("/product")
async def create_product(product: Product):
    if (product.id in products):
        raise HTTPException(status_code=404, detail="product already exists")
    else:
        products[product.id] = product
        return product

# PATCH -> atualiza produto com modificações desejadas
@app.patch("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product):
    if (product_id in products):
        stored_product_data = products[product_id]
        stored_product_model = Product(**stored_product_data)
        update_data = product.dict(exclude_unset=True)
        updated_product = stored_product_model.copy(update=update_data)
        products[product_id] = jsonable_encoder(updated_product)
        return updated_product
    else:
        raise HTTPException(status_code=404, detail="product does not exist")

# GET -> recebe o produto
@app.get("/product/{product_id}")
async def get_product(product_id: int):
    if (product_id in products):
        return products[product_id]
    else :
        raise HTTPException(status_code=404, detail="product does not exist")

# DELETE -> apaga o produto
@app.delete("/product")
async def delete_product(product_id: int):
    if (product_id in products) :
        del products[product_id]
        return products
    else :
        raise HTTPException(status_code=404, detail="product does not exist")

@app.get("/")
async def root():
    return {"message": "welcome to our inventory API"}