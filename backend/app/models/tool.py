from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base


class Custom(Base):
    """春节习俗数据模型
    
    存储各种春节习俗的详细说明。
    """
    __tablename__ = "customs"
    
    id = Column(Integer, primary_key=True, index=True)  # 习俗 ID
    title = Column(String(200), nullable=False)  # 习俗标题
    category = Column(String(50))   # 习俗分类
    content = Column(Text, nullable=False)  # 习俗内容
    region = Column(String(50), default="general")  # 适用地区
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间


class Etiquette(Base):
    """拜年礼仪数据模型
    
    存储各种场景下的拜年礼仪规范。
    """
    __tablename__ = "etiquettes"
    
    id = Column(Integer, primary_key=True, index=True)  # 礼仪 ID
    title = Column(String(200), nullable=False)  # 礼仪标题
    category = Column(String(50))  # 礼仪分类
    content = Column(Text, nullable=False)  # 礼仪内容
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间


class GiftSuggestion(Base):
    """礼物建议数据模型
    
    存储针对不同群体的春节礼物推荐。
    """
    __tablename__ = "gift_suggestions"
    
    id = Column(Integer, primary_key=True, index=True)  # 建议 ID
    target_group = Column(String(50))  # 目标群体
    gift_name = Column(String(200))  # 礼物名称
    description = Column(Text)  # 礼物描述
    price_range = Column(String(50))  # 价格范围
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
