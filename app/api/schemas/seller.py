from pydantic import BaseModel, EmailStr, ConfigDict

class BaseSeller(BaseModel):
    name: str
    email: EmailStr

class SellerRead(BaseSeller):
    model_config = ConfigDict(from_attributes=True)

class SellerCreate(BaseSeller):
    password: str