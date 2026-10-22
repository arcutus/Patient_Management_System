from .usermodel import UserSchema
from sqlalchemy.orm import Session


def register(body: UserSchema, db: Session):
    print(body)
    return {"msg": "Registration Done"}
