from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class MembershipType(enum.Enum):
    """会员类型枚举
    
    定义用户的会员等级类型。
    """
    FREE = "free"  # 免费用户
    VIP = "vip"    # VIP 会员


class User(Base):
    """用户数据模型
    
    存储用户的基本信息和会员状态。
    支持通过手机号或微信 openid 登录。
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)  # 用户 ID
    openid = Column(String(100), unique=True, index=True, nullable=True)  # 微信 openid
    phone = Column(String(20), unique=True, index=True, nullable=True)  # 手机号
    username = Column(String(50))  # 用户昵称
    avatar = Column(String(255), nullable=True)  # 头像 URL
    membership_type = Column(Enum(MembershipType), default=MembershipType.FREE)  # 会员类型
    vip_expire_time = Column(DateTime, nullable=True)  # VIP 过期时间
    is_active = Column(Boolean, default=True)  # 是否激活
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # 更新时间
