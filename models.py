from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

import database


class Product(database.Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    description = Column(String(255))
    price = Column(Float, default=True)
    quantity = Column(Integer, default=True)
    removed = Column(Boolean)


class Inventory(database.Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))

    rel = relationship("Product", backref="inventory", primaryjoin="Product.id == Inventory.product_id")