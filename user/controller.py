from .usermodel import UserSchema
from sqlalchemy.orm import Session
from .login import UserModel
from fastapi import HTTPException
from pwdlib import PasswordHash

password_hash=PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)


def register(body: UserSchema, db: Session):
    print(body)

    #username validation
    #email validation
    is_user=db.query(UserModel).filter(UserModel.username==body.username).first()
    if is_user:
        raise HTTPException(400,detail="username already exist")
   
    is_user=db.query(UserModel).filter(UserModel.email==body.email).first()
    if is_user:
        raise HTTPException(400,detail="email already exist")

    hash_password=get_password_hash(body.password)

    new_user=UserModel(
        name=body.name,
        username=body.username,
        hash_password=hash_password,
        email=body.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "name": new_user.name,
        "username": new_user.username,
        "email": new_user.email,
    }
