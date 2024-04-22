from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from sqlalchemy.sql.expression import select
from typing import List
from app.core.database import get_db
from app.models import models
from app.api.schemas import schemas


router = APIRouter(
    tags=['Products'],
)


@router.get("/", status_code=status.HTTP_200_OK ,response_model=List[schemas.ProductWithImage])
def all(limit: int = 0, db: Session = Depends(get_db)):
    try:
        subquery = select(models.ProductPhoto.product_id, func.min(models.ProductPhoto.url).label("first_photo_url")).group_by(models.ProductPhoto.product_id).subquery()
        products = db.query(
                models.Product.id,
                models.Product.name,
                models.Product.description,
                models.Product.price,
                models.Product.discount,
                func.coalesce(subquery.c.first_photo_url, "").label("url")
            ).outerjoin(subquery, models.Product.id == subquery.c.product_id).all()
        if limit > 0:
            products = products[:limit]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return products

def get_product_details(db: Session, product_id: int):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == product_id)
        .options(
            joinedload(models.Product.photos),
            joinedload(models.Product.colors),
            joinedload(models.Product.sizes),
            joinedload(models.Product.brand),
            joinedload(models.Product.category),
            joinedload(models.Product.subcategory)
        )
        .first()
    )

    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return {
        "product": product,
        "photos": product.photos,
        "colors": product.colors,
        "sizes": product.sizes,
        "brand": product.brand,
        "category": product.category,
        "subcategory": product.subcategory
    }

@router.get('/product/{id}')
def get(id: int, db: Session = Depends(get_db)):
    product_details = get_product_details(db, id)
    return product_details