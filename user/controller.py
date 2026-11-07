import logging

from fastapi import BackgroundTasks, HTTPException, Request
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from myenv.database import ALGORITHM, EXP_TIME, SECRET_KEY
from .registertable import UserModel
from .usermodel import LoginSchema, UserSchema
from datetime import datetime, timedelta, timezone
from .mail import send_email

password_hash = PasswordHash.recommended()
logger = logging.getLogger(__name__)


async def send_registration_email(email: str) -> None:
    try:
        await send_email([email])
    except Exception:
        logger.exception("Failed to send registration confirmation email")
    else:
        print("Registration confirmation email sent successfully")


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


async def register(body: UserSchema, db: Session, background_tasks: BackgroundTasks):
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

    background_tasks.add_task(send_registration_email, new_user.email)
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

    # Set expiration time in UTC
    exp_time = datetime.now(timezone.utc) + timedelta(minutes=EXP_TIME)

    token = jwt.encode(
        {"_id": user.id, "exp": exp_time},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return {"token": token}


def is_authenticated(request: Request, db: Session):
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(401, detail="authorization header missing")

    try:
        scheme, token = auth_header.split(" ", 1)
    except ValueError:
        raise HTTPException(401, detail="invalid authorization header")

    if scheme.lower() != "bearer" or not token:
        raise HTTPException(401, detail="invalid token format")

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="invalid token")

    # Verify that the user still exists in the database
    user = db.query(UserModel).filter(UserModel.id == data.get("_id")).first()
    if not user:
        raise HTTPException(401, detail="user no longer exists")

    return {"message": "Authenticated successfully", "user": {"id": user.id, "username": user.username}}
