from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
class EmailSchema(BaseModel):
    email:List[EmailStr]

conf=ConnectionConfig(
    MAIL_USERNAME = "tintinarcutu@email.com",
    MAIL_PASSWORD = "gmcd enme edtp rqtj",
    MAIL_FROM = "tintinarcutu@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Patient_Management_System",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
