from fastapi import APIRouter, Depends, status,Request
from sqlalchemy.orm import Session

from .usermodel import UserResponseSchema, UserSchema, LoginSchema
from . import controller
from myenv.db import get_db

user_router = APIRouter(prefix="/user")


@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def registration(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register(body, db)


@user_router.post("/login", status_code=status.HTTP_200_OK)
def login(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)


@user_router.get("/is_auth",status_code=status.HTTP_200_OK)
def is_auth(request:Request,db: Session = Depends(get_db)):
    return controller.is_authenticated(request,db)
