from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum


class TargetGroup(enum.Enum):
    """目标群体枚举
    
    定义祝福语的适用对象群体。
    """
    ELDER = "elder"      # 长辈
    LEADER = "leader"    # 领导
    COLLEAGUE = "colleague"  # 同事
    FRIEND = "friend"    # 朋友
    TEACHER = "teacher"  # 老师
    GENERAL = "general"  # 通用


class StyleType(enum.Enum):
    """风格类型枚举
    
    定义祝福语的语言风格。
    """
    FORMAL = "formal"    # 正式稳重
    HIGH_EQ = "high_eq"   # 高情商
    SHORT = "short"       # 简短高级
    HUMOR = "humor"      # 幽默搞笑
    WARM = "warm"        # 温暖走心
    CLASSIC = "classic"   # 古风文雅
    BUSINESS = "business"  # 商务官方
    CUTE = "cute"        # 可爱俏皮


class FormatType(enum.Enum):
    """格式类型枚举
    
    定义祝福语的输出格式。
    """
    SENTENCE = "sentence"    # 短句类
    LONG = "long"            # 长文类
    COUPLET = "couplet"      # 对联类
    MOMENTS = "moments"      # 朋友圈
    VIDEO = "video"          # 视频文案
    RED_PACKET = "red_packet"  # 红包封面


class Greeting(Base):
    """祝福语数据模型
    
    存储生成的祝福语内容及其分类信息。
    """
    __tablename__ = "greetings"
    
    id = Column(Integer, primary_key=True, index=True)  # 祝福语 ID
    content = Column(Text, nullable=False)  # 祝福语内容
    target_group = Column(Enum(TargetGroup), nullable=False)  # 目标群体
    style = Column(Enum(StyleType), nullable=False)  # 风格类型
    format_type = Column(Enum(FormatType), nullable=False)  # 格式类型
    zodiac_year = Column(String(10), default="2026")  # 生肖年份
    is_vip_only = Column(Boolean, default=False)  # 是否仅 VIP 可用
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 创建时间


class UserGreeting(Base):
    """用户收藏祝福语关联模型
    
    存储用户收藏的祝福语记录。
    """
    __tablename__ = "user_greetings"
    
    id = Column(Integer, primary_key=True, index=True)  # 关联 ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 用户 ID
    greeting_id = Column(Integer, ForeignKey("greetings.id"), nullable=False)  # 祝福语 ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 收藏时间
