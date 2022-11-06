from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import utils, models, schemas
import database

models.database.Base.metadata.create_all(bind=database.engine)
from fastapi.encoders import jsonable_encoder

#######################################

app = FastAPI()

###################################### INICIALIZANDO PRODUTO E ESTOQUE ######################################

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

###################################### INPLEMENTAÇÃO DO CRUD ######################################

# GET -> mostra o estoque com os produtos
@app.get("/inventory/all")
async def list_inventory(db: Session = Depends(get_db)):
    inventory = utils.fetch_inventory(db)
    return inventory

# GET -> todos os produtos do estoque
@app.get("/product/all")
async def list_products(db: Session = Depends(get_db)):
    products = utils.get_products(db)
    return products

#POST -> movimentação dos produtos dentro do estoque; adicionar produtos etc
@app.post("/product/transaction")
async def product_transaction(movement: schemas.Inventory, db: Session = Depends(get_db)):
    product_id = movement.product_id
    qty = movement.quantity

    if (product_id in products):
        product = dict( products[product_id] )

        # Condição para tratar estoque negativo.
        if product['quantity'] + qty >= 0:
            new_qty = product['quantity'] + qty
            product['quantity'] = new_qty
        else:
            raise HTTPException(status_code=404, detail="can't move quantity")
        
        products[product_id] = jsonable_encoder(product)

        inventory.append({"product_id" : product_id, "quantity" : qty}) 
        return product
    else:
        raise HTTPException(status_code=404, detail="product does not exist")

# POST -> cria um produto qualquer
@app.post("/product")
async def create_product(product: schemas.Product, db: Session = Depends(get_db)):
    existing_product = utils.get_product_by_name(db, name=product.name)
    if existing_product: 
        raise HTTPException(status_code=404, detail="product already exists")
    
    return utils.create_product(db=db, product=product)

# # PATCH -> atualiza produto com modificações desejadas
# @app.patch("/product/{product_id}", response_model=Product)
# async def update_product(product_id: int, product: Product):
#     if (product_id in products):
#         stored_product_data = products[product_id]
#         stored_product_model = Product(**stored_product_data)
#         update_data = product.dict(exclude_unset=True)
#         updated_product = stored_product_model.copy(update=update_data)
#         products[product_id] = jsonable_encoder(updated_product)
#         return updated_product
#     else:
#         raise HTTPException(status_code=404, detail="product does not exist")

# GET -> busca o produto
@app.get("/product/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = utils.get_product(db, product_id=product_id)
    if product: return product

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