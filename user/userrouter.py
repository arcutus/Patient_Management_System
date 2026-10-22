from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from .usermodel import UserResponseSchema, UserSchema
from myenv.db import get_db
from. import controller



user_router=APIRouter(prefix="/user")

@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def registation(body:UserSchema,db:Session=Depends(get_db)):
    return controller.register(body,db)
