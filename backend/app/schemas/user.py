from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from ..models.user import MembershipType


class UserBase(BaseModel):
    username: Optional[str] = None
    avatar: Optional[str] = None


class UserCreate(UserBase):
    phone: Optional[str] = None
    openid: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(UserBase):
    id: int
    membership_type: MembershipType
    vip_expire_time: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginRequest(BaseModel):
    phone: Optional[str] = None
    openid: Optional[str] = None
    code: Optional[str] = None
