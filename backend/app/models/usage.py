from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..core.database import Base


class UsageLog(Base):
    """用户使用日志数据模型
    
    记录用户对各个功能的使用次数，用于统计和限流。
    """
    __tablename__ = "usage_logs"
    
    id = Column(Integer, primary_key=True, index=True)  # 日志 ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 用户 ID
    feature = Column(String(50), nullable=False)  # 功能名称
    usage_count = Column(Integer, default=1)  # 使用次数
    date = Column(String(20), nullable=False)  # 日期（格式：YYYY-MM-DD）
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
