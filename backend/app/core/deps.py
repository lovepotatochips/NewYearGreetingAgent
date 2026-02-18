from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from .database import get_db
from .security import decode_access_token
from ..models.user import User
from ..services.user_service import UserService

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户
    
    从 HTTP Bearer 令牌中解析用户信息并返回。
    如果令牌无效或用户不存在，抛出 401 异常。
    
    Args:
        credentials: HTTP Bearer 认证凭据
        db: 数据库会话
    
    Returns:
        User: 当前登录的用户对象
    
    Raises:
        HTTPException: 令牌无效或用户不存在时抛出 401 异常
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(int(user_id))
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取当前激活用户
    
    依赖 get_current_user，额外检查用户是否处于激活状态。
    
    Args:
        current_user: 当前用户对象
    
    Returns:
        User: 激活状态的用户对象
    
    Raises:
        HTTPException: 用户未激活时抛出 400 异常
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user


async def check_vip_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> User:
    """检查并获取 VIP 用户
    
    依赖 get_current_active_user，额外检查用户是否为 VIP 会员。
    非会员用户访问 VIP 功能时抛出 403 异常。
    
    Args:
        current_user: 当前激活用户对象
        db: 数据库会话
    
    Returns:
        User: VIP 用户对象
    
    Raises:
        HTTPException: 用户不是 VIP 时抛出 403 异常
    """
    user_service = UserService(db)
    if not user_service.check_vip_status(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="此功能需要VIP会员"
        )
    return current_user


def get_client_ip(request) -> str:
    """获取客户端 IP 地址
    
    从请求头或请求对象中提取客户端的真实 IP 地址。
    支持代理转发的情况（X-Forwarded-For 头）。
    
    Args:
        request: FastAPI 请求对象
    
    Returns:
        str: 客户端的 IP 地址字符串
    """
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host
