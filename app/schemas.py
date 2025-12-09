from pydantic import BaseModel

class UserLogin(BaseModel):
    login: str
    password: str

class UserRegister(BaseModel):
    fio: str
    phone_number: str
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
    role: str