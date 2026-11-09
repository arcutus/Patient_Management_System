import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

# Load environment variables from .env in project root
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=ROOT_DIR / ".env")


def get_mail_config() -> ConnectionConfig:
    username = os.getenv("MAIL_USERNAME")
    raw_password = os.getenv("MAIL_PASSWORD")
    mail_from = os.getenv("MAIL_FROM")

    missing = []
    if not username:
        missing.append("MAIL_USERNAME")
    if not raw_password:
        missing.append("MAIL_PASSWORD")
    if not mail_from:
        missing.append("MAIL_FROM")

    if missing:
        raise RuntimeError(
            f"Missing required email configuration in .env: {', '.join(missing)}"
        )

    # Remove any accidental spaces in the app password
    password = raw_password.replace(" ", "")

    mail_port = int(os.getenv("MAIL_PORT", "465"))
    mail_server = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    mail_from_name = os.getenv("MAIL_FROM_NAME", "Patient_Management_System")
    mail_ssl_tls = os.getenv("MAIL_SSL_TLS", "True").lower() in ("true", "1", "yes")
    mail_starttls = os.getenv("MAIL_STARTTLS", "False").lower() in ("true", "1", "yes")

    return ConnectionConfig(
        MAIL_USERNAME=username,
        MAIL_PASSWORD=password,
        MAIL_FROM=mail_from,
        MAIL_PORT=mail_port,
        MAIL_SERVER=mail_server,
        MAIL_FROM_NAME=mail_from_name,
        MAIL_STARTTLS=mail_starttls,
        MAIL_SSL_TLS=mail_ssl_tls,
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
