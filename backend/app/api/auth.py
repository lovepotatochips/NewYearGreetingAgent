from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_user
from ..schemas.user import LoginRequest, Token, UserResponse
from ..models.user import User
from ..services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=Token)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户登录接口
    
    支持通过手机号或 openid 进行登录。
    如果用户不存在，会自动创建新用户。
    
    Args:
        request: 登录请求，包含 phone 或 openid
        db: 数据库会话
    
    Returns:
        Token: 包含访问令牌和用户信息的响应
    
    Raises:
        HTTPException: 未提供认证信息或用户被禁用时抛出异常
    """
    user_service = UserService(db)
    
    if request.openid:
        user = user_service.get_or_create_user(
            LoginRequest(openid=request.openid)
        )
    elif request.phone:
        user = user_service.get_or_create_user(
            LoginRequest(phone=request.phone, username=request.phone[:4] + "****")
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供手机号或openid"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    access_token = user_service.create_token(user.id)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息
    
    返回已登录用户的详细信息。
    
    Args:
        current_user: 当前登录用户（通过依赖注入获取）
    
    Returns:
        UserResponse: 用户信息响应对象
    """
    return UserResponse.model_validate(current_user)


@router.post("/register", response_model=Token)
async def register(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """用户注册接口
    
    创建新用户账号，并返回访问令牌。
    检查手机号或 openid 是否已被注册。
    
    Args:
        request: 注册请求，包含 phone 或 openid
        db: 数据库会话
    
    Returns:
        Token: 包含访问令牌和新用户信息的响应
    
    Raises:
        HTTPException: 手机号或 openid 已存在时抛出异常
    """
    user_service = UserService(db)
    
    if request.phone and user_service.get_user_by_phone(request.phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已被注册"
        )
    
    if request.openid and user_service.get_user_by_openid(request.openid):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="openid已被注册"
        )
    
    user = user_service.create_user(request)
    access_token = user_service.create_token(user.id)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse.model_validate(user)
    )
