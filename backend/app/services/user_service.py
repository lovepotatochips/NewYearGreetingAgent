from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..models.user import User, MembershipType
from ..core.security import get_password_hash, verify_password, create_access_token
from ..schemas.user import UserCreate, UserResponse


class UserService:
    """用户服务类
    
    负责用户相关的业务逻辑，包括用户查询、创建、更新、
    VIP 会员管理和令牌生成等功能。
    """
    
    def __init__(self, db: Session):
        """初始化用户服务
        
        Args:
            db: SQLAlchemy 数据库会话
        """
        self.db = db
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """根据用户 ID 查询用户
        
        Args:
            user_id: 用户 ID
        
        Returns:
            Optional[User]: 用户对象，不存在时返回 None
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """根据手机号查询用户
        
        Args:
            phone: 手机号
        
        Returns:
            Optional[User]: 用户对象，不存在时返回 None
        """
        return self.db.query(User).filter(User.phone == phone).first()
    
    def get_user_by_openid(self, openid: str) -> Optional[User]:
        """根据 openid 查询用户
        
        Args:
            openid: 微信 openid
        
        Returns:
            Optional[User]: 用户对象，不存在时返回 None
        """
        return self.db.query(User).filter(User.openid == openid).first()
    
    def create_user(self, user_data: UserCreate) -> User:
        """创建新用户
        
        根据提供的数据创建新用户账号。
        
        Args:
            user_data: 用户创建数据
        
        Returns:
            User: 创建的用户对象
        """
        db_user = User(
            openid=user_data.openid,
            phone=user_data.phone,
            username=user_data.username,
            avatar=user_data.avatar
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_or_create_user(self, user_data: UserCreate) -> User:
        """获取或创建用户
        
        如果用户已存在则返回，不存在则创建新用户。
        用于登录时的用户处理逻辑。
        
        Args:
            user_data: 用户数据（手机号或 openid）
        
        Returns:
            User: 用户对象
        
        Raises:
            ValueError: 未提供手机号或 openid 时抛出异常
        """
        if user_data.phone:
            user = self.get_user_by_phone(user_data.phone)
        elif user_data.openid:
            user = self.get_user_by_openid(user_data.openid)
        else:
            raise ValueError("Must provide either phone or openid")
        
        if user:
            return user
        
        return self.create_user(user_data)
    
    def update_user(self, user_id: int, username: str = None, avatar: str = None) -> Optional[User]:
        """更新用户信息
        
        更新用户的昵称或头像信息。
        
        Args:
            user_id: 用户 ID
            username: 新昵称（可选）
            avatar: 新头像 URL（可选）
        
        Returns:
            Optional[User]: 更新后的用户对象
        """
        user = self.get_user_by_id(user_id)
        if user:
            if username:
                user.username = username
            if avatar:
                user.avatar = avatar
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def set_vip(self, user_id: int, days: int = 30) -> Optional[User]:
        """设置用户为 VIP 会员
        
        将用户升级为 VIP 会员，并设置过期时间。
        
        Args:
            user_id: 用户 ID
            days: VIP 有效天数，默认 30 天
        
        Returns:
            Optional[User]: 更新后的用户对象
        """
        user = self.get_user_by_id(user_id)
        if user:
            user.membership_type = MembershipType.VIP
            user.vip_expire_time = datetime.utcnow() + timedelta(days=days)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def check_vip_status(self, user_id: int) -> bool:
        """检查用户 VIP 状态
        
        检查用户是否为有效的 VIP 会员。
        如果 VIP 已过期，自动降级为普通用户。
        
        Args:
            user_id: 用户 ID
        
        Returns:
            bool: 是有效 VIP 返回 True，否则返回 False
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        if user.membership_type == MembershipType.VIP:
            if user.vip_expire_time and user.vip_expire_time > datetime.utcnow():
                return True
            else:
                user.membership_type = MembershipType.FREE
                self.db.commit()
        return False
    
    def create_token(self, user_id: int) -> str:
        """为用户创建访问令牌
        
        生成 JWT 访问令牌用于用户认证。
        
        Args:
            user_id: 用户 ID
        
        Returns:
            str: JWT 访问令牌字符串
        """
        return create_access_token(data={"sub": str(user_id)})


def get_user_service(db: Session) -> UserService:
    """获取用户服务实例
    
    Args:
        db: 数据库会话
    
    Returns:
        UserService: 用户服务实例
    """
    return UserService(db)
