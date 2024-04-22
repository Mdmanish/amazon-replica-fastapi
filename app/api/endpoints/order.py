from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.core.database import get_db
from app.models import models
from app.api.schemas import order
from typing import List


router = APIRouter(
    tags=["Order"],
)


@router.post("/order", status_code=status.HTTP_201_CREATED)
def create_order(request: order.Order, db: Session = Depends(get_db)):
    db_order = models.Order(**request.dict(exclude={"items"}))
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in request.items:
        db_order_item = models.OrderItem(order_id=db_order.id, **item.dict())
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/order/{user_id}" , status_code=status.HTTP_200_OK)
def get_order(user_id: int, db: Session = Depends(get_db)):
    active_orders_subquery = db.query(models.Order.id).filter(models.Order.user_id == user_id, models.Order.active == True).subquery()
    query = (
        db.query(models.OrderItem)
        .join(active_orders_subquery, active_orders_subquery.c.id == models.OrderItem.order_id)
        .join(models.Product, models.Product.id == models.OrderItem.product_id)
        .join(models.ProductPhoto, models.ProductPhoto.product_id == models.Product.id)
        .filter(models.OrderItem.active == True)
        .options(joinedload(models.OrderItem.product).joinedload(models.Product.photos))
    )

    results = query.all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return results


@router.patch("/order/{order_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_item_id: int, db: Session = Depends(get_db)):
    order = db.query(models.OrderItem).filter(models.OrderItem.id == order_item_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    order.active = False
    db.add(order)
    db.commit()
    return {"message": "Order cancelled successfully"}
