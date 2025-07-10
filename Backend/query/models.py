from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    balance: float
    po_status: str
    po_value: float
    po_number: int
    supplier: str
    quantity: int
    order_description: str

    class Config:
        orm_mode = True
        
class NameRequest(BaseModel):
    name: str
    
class NlpRequest(BaseModel):
    question: str
    name: str
    
class StatusRequest(BaseModel):
    status: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class LoginRequest(BaseModel):
    username: str
    password: str

class StatusCountResponse(BaseModel):
    count: int
