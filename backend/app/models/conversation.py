from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Conversation(Base):
    """对话数据模型
    
    存储用户的对话会话信息。
    每个对话包含多条消息记录。
    """
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)  # 对话 ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 用户 ID
    title = Column(String(200), default="新对话")  # 对话标题
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间
    
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")  # 关联的消息列表


class Message(Base):
    """消息数据模型
    
    存储对话中的单条消息。
    消息可以是用户发送的，也可以是 AI 回复的。
    """
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)  # 消息 ID
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)  # 对话 ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 用户 ID
    role = Column(String(20))   # 消息角色（user/assistant）
    content = Column(Text)  # 消息内容
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    
    conversation = relationship("Conversation", back_populates="messages")  # 关联的对话
