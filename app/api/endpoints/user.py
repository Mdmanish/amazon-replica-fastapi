from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models
from app.api.schemas import user
from app.core.hashing import Hash
from typing import List


router = APIRouter(
    tags=["user"],
)


@router.post("/address", status_code=status.HTTP_201_CREATED)
def create_address(request: user.UserAddress, db: Session = Depends(get_db)):
    db_address = models.UserAddress(**request.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

@router.get("/address/{user_id}" , status_code=status.HTTP_200_OK, response_model=List[user.UserAddressResponse])
def get_address(user_id: int, db: Session = Depends(get_db)):
    print('inside get: ', user_id)
    address = db.query(models.UserAddress).filter(models.UserAddress.user_id == user_id)
    if not address:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    return address
