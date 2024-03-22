from sqlalchemy.orm import Session

from app.crud import models
from app.crud.schemas import ProductBase


def create_product(db: Session, product: ProductBase):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def update_product(db: Session, product_id: int, product_data: ProductBase):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product_data.dict().items():
            setattr(db_product, key, value)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None


def delete_product(db: Session, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
