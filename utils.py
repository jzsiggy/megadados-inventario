from sqlalchemy.orm import Session

import models, schemas


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_name(db: Session, name: str):
    return db.query(models.Product).filter(models.Product.name == name).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def fetch_inventory(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Inventory).offset(skip).limit(limit).all()

def create_inventory_movement(db: Session, movement: schemas.Inventory):
    db_movement = models.Inventory(product_id=movement.product_id, quantity=movement.quantity)
    db.add(db_movement)
    db.commit()
    db.refresh(db_movement)
    return db_movement

def create_product(db: Session, product: schemas.Product):
    db_product = models.Product(name=product.name, description=product.description, price=product.price, quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    return

def update_product(db: Session, product_id: int, product: schemas.Product):
    return