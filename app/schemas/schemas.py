from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.models.enums import TransactionType, TransactionStatus

# User Schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# Wallet Schemas
class WalletCreate(BaseModel):
    user_id: int

class WalletResponse(BaseModel):
    id: int
    user_id: int
    balance: float
    
    class Config:
        from_attributes = True

class WalletBalanceResponse(BaseModel):
    wallet_id: int
    balance: float

# Transaction Schemas
class TransactionBase(BaseModel):
    user_id: int
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    description: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class FundsRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID must be greater than 0")
    amount: float = Field(..., gt=0, description="Amount must be greater than 0")
    description: Optional[str] = Field(None, max_length=255)

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    amount: float
    timestamp: datetime
    status: TransactionStatus
    description: Optional[str] = None
    
    class Config:
        from_attributes = True

class TransactionHistoryResponse(BaseModel):
    user_id: int
    transactions: List[TransactionResponse]

# Error Response Schema
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None
