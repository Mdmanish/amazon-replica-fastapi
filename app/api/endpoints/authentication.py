from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import models
from app.core.hashing import Hash
from app.api.schemas import schemas
from app.core import token, oauth2
# from app.core.security import create_access_token
# from app.schemas import tokens


router = APIRouter(
    tags=["authentication"],
)


@router.post("/login")
def login(request: schemas.LoginUser, db: Session = Depends(get_db)):
    if request.username == "" or request.password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")
    user = db.query(models.User).filter(models.User.mobile == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not Hash.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = token.create_access_token(data={'sub': user.mobile})
    return {"access_token": access_token, "token_type": "bearer"}
    # return user


@router.post("/register")
def register(request: schemas.RegisterUser, db: Session = Depends(get_db)):
    if request.name == "" or request.username == "" or request.password == "" or request.confirm_password == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All fields are required")
    if len(request.username) != 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mobile number must be 10 digits")
    if db.query(models.User).filter(models.User.mobile == request.username).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    if request.password != request.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    new_user = models.User(name=request.name, mobile=request.username, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@router.post("/get_user", response_model=schemas.ResponseUser)
def get_user(request: schemas.Token, db: Session = Depends(get_db)):
    print('inside get user')
    user = oauth2.get_current_user(request.access_token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    user = db.query(models.User).filter(models.User.mobile == user.email).first()
    return user
