from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List
from starlette.responses import JSONResponse



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


@app.post("/email")
async def send(emails:List[str]) -> JSONResponse:
    html = """<p>Hi this test mail, thanks for using Fastapi-mail</p> """

    message = MessageSchema(
        subject="Registration Confirmation",
        recipients=emails,
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})