from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from ..models.greeting import TargetGroup, StyleType, FormatType


class GreetingBase(BaseModel):
    content: str
    target_group: TargetGroup
    style: StyleType
    format_type: FormatType


class GreetingCreate(BaseModel):
    target_group: TargetGroup
    style: StyleType
    format_type: FormatType
    custom_content: Optional[str] = None
    keywords: Optional[List[str]] = None


class GreetingResponse(GreetingBase):
    id: int
    zodiac_year: str
    is_vip_only: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class GreetingOptimizeRequest(BaseModel):
    content: str
    target_style: Optional[StyleType] = None
    target_group: Optional[TargetGroup] = None
    length_adjust: Optional[str] = None
    avoid_duplicate: bool = False


class GreetingGenerateRequest(BaseModel):
    target_group: TargetGroup
    style: StyleType
    format_type: FormatType
    keywords: Optional[List[str]] = None
    count: int = Field(default=1, ge=1, le=20)


class CustomGreetingRequest(BaseModel):
    recipient_info: str
    relationship: str
    style: StyleType
    length: Optional[int] = None
    keywords: Optional[List[str]] = None
