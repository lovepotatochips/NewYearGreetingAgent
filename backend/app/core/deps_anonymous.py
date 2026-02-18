from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .security import decode_access_token
from ..models.user import User
from ..services.user_service import UserService

security = HTTPBearer(auto_error=False)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选的用户
    
    尝试从 HTTP 令牌中获取用户，但如果令牌不存在或无效，
    不会抛出异常，而是返回 None。
    
    Args:
        credentials: 可选的 HTTP Bearer 认证凭据
        db: 数据库会话
    
    Returns:
        Optional[User]: 用户对象，未认证时返回 None
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        return None
    
    user_id: str = payload.get("sub")
    if user_id is None:
        return None
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(int(user_id))
    
    return user


async def get_anonymous_or_user(
    optional_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
) -> User:
    """获取匿名用户或已登录用户
    
    如果用户已登录则返回该用户，否则返回或创建匿名用户。
    这样可以支持未登录用户使用某些基础功能。
    
    Args:
        optional_user: 可选的用户对象（可能为 None）
        db: 数据库会话
    
    Returns:
        User: 用户对象（已登录用户或匿名用户）
    """
    if optional_user:
        return optional_user
    
    user_service = UserService(db)
    anonymous_user = user_service.get_user_by_phone("anonymous")
    
    if not anonymous_user:
        from ..schemas.user import UserCreate
        anonymous_user = user_service.create_user(
            UserCreate(phone="anonymous", username="匿名用户")
        )
    
    return anonymous_user
