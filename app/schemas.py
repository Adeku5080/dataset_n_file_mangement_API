from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    fullname: str
    email: EmailStr
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
