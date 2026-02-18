from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    role: str
    content: str


class MessageCreate(MessageBase):
    pass


class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    title: str = "新对话"


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None


class ConversationResponse(ConversationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    voice_mode: bool = False
