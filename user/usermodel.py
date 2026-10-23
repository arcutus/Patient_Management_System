from pydantic import BaseModel, field_validator


class UserSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, email: str) -> str:
        email = email.strip()
        if not email.casefold().endswith("@gmail.com"):
            raise ValueError("Email must end with @gmail.com")
        return email

class UserResponseSchema(BaseModel):
    name:str
    username:str
    email:str
    id:str
    
    

#libraries  like pwjt and pwlib  was istalled on the termina for this

class LoginSchema(BaseModel):
    username:str
    password:str