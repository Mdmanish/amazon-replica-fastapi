from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.api.endpoints import authentication, home, user, cart, order
from app import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000','https://amazon-replica-manish.netlify.app'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(home.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(order.router)
