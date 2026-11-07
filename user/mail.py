import os
from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType


def get_mail_config() -> ConnectionConfig:
    username = os.getenv("MAIL_USERNAME") or "tintinarcutu@gmail.com"
    password = os.getenv("MAIL_PASSWORD") or "gmcd enme edtp rqtj"
    mail_from = os.getenv("MAIL_FROM") or "tintinarcutu@gmail.com"

    return ConnectionConfig(
        MAIL_USERNAME=username,
        MAIL_PASSWORD=password,
        MAIL_FROM=mail_from,
        MAIL_PORT=587,
        MAIL_SERVER="smtp.gmail.com",
        MAIL_FROM_NAME="Patient_Management_System",
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )


async def send_email(emails: List[str]) -> None:
    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body="<p>Hi, thanks for using Patient Management System.</p>",
        subtype=MessageType.html,
    )
    await FastMail(get_mail_config()).send_message(message)
