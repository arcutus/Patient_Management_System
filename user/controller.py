from .usermodel import UserSchema

def register(body: UserSchema) -> UserSchema:
   print(body)
   return{"msg":"Registration Done"}
