from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models import models
from app.api.schemas import cart
from typing import List


router = APIRouter(
    tags=["Cart"],
)


@router.post("/cart", status_code=status.HTTP_201_CREATED)
def create_cart(request: cart.Cart, db: Session = Depends(get_db)):
    db_cart = models.Cart(**request.dict())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


@router.get("/cart/{user_id}" , status_code=status.HTTP_200_OK)
def get_cart(user_id: int, db: Session = Depends(get_db)):
    print('inside get: ', user_id)
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).options(
        joinedload(models.Cart.product).joinedload(models.Product.photos)
    ).all()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    return cart

@router.delete("/cart/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(cart_id: int, db: Session = Depends(get_db)):
    cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    db.delete(cart)
    db.commit()
    return {"message": "Cart deleted successfully"}

@router.delete("/cart/bulk-delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carts(user_id: int, db: Session = Depends(get_db)):
    carts = db.query(models.Cart).filter(models.Cart.user_id == user_id)
    if not carts.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carts not found")
    delete_count = carts.delete()
    if delete_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carts not found")
    db.commit()
    return {"message": "Carts deleted successfully"}
