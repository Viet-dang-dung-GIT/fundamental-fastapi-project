from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from app.crud import schemas
from app.crud.database import get_db
from app.crud.crud_products import delete_product, get_product, update_product, create_product as create

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


@router.get("/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    return product


@router.post("/", response_model=schemas.ProductBase)
def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    set_product = create(db, product)
    return set_product


@router.put("/{product_id}", response_model=schemas.Product)
def update_existing_product(product_id: int, product: schemas.ProductBase, db: Session = Depends(get_db)):
    updated_product = update_product(db, product_id, product)
    return updated_product


@router.delete("/{product_id}", response_model=schemas.Product)
def delete_existing_product(product_id: int, db: Session = Depends(get_db)):
    deleted_product = delete_product(db, product_id)
    return deleted_product
