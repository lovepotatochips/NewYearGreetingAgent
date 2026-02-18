from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class Knowledge(Base):
    """知识库数据模型
    
    存储春节相关的知识问答。
    用于快速响应用户关于习俗、礼仪等问题。
    """
    __tablename__ = "knowledge"
    
    id = Column(Integer, primary_key=True, index=True)  # 知识 ID
    category = Column(String(50), nullable=False)  # 分类（习俗、礼仪、礼物等）
    keywords = Column(Text, nullable=False)  # 关键词（逗号分隔）
    question = Column(Text, nullable=False)  # 问题
    answer = Column(Text, nullable=False)  # 答案
    priority = Column(Integer, default=0)  # 优先级（数值越大越优先）
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间
