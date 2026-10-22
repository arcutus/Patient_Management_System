from pydantic import BaseModel

class UserSchema(BaseModel):
    name:str
    username:str
    password:str
    email:str

#libraries  like pwjt and pwlib  was istalled on the termina for this
