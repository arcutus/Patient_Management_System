from fastapi import HTTPException
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from myenv.database import ALGORITHM, EXP_TIME, SECRET_KEY
from .register import UserModel
from .usermodel import LoginSchema, UserSchema
from datetime import datetime, timedelta


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)


def register(body: UserSchema, db: Session):
    print(body)

    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        raise HTTPException(400, detail="username already exist")

    is_user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_user:
        raise HTTPException(400, detail="email already exist")

    hash_password = get_password_hash(body.password)

    new_user = UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "username": new_user.username,
        "email": new_user.email,
    }


def login_user(body: LoginSchema, db: Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if not user:
        raise HTTPException(404, detail="user not found")

    if not password_hash.verify(body.password, user.hash_password):
        raise HTTPException(401, detail="invalid password")

    exp_time = datetime.now() + timedelta(minutes=EXP_TIME)
    
    
    
    token = jwt.encode({"_id": user.id,"exp":exp_time}, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"token":token}