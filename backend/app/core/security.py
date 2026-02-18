from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码
    
    使用 bcrypt 算法验证用户输入的密码是否与存储的哈希密码匹配。
    
    Args:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的哈希密码
    
    Returns:
        bool: 密码匹配返回 True，否则返回 False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希
    
    使用 bcrypt 算法将明文密码转换为哈希密码，
    用于在数据库中安全存储用户密码。
    
    Args:
        password: 明文密码
    
    Returns:
        str: 哈希后的密码字符串
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌
    
    使用 JWT（JSON Web Token）生成用户访问令牌。
    令牌包含用户数据，并在指定时间后过期。
    
    Args:
        data: 要编码到令牌中的数据，通常包含用户 ID
        expires_delta: 自定义过期时间，不指定则使用默认配置
    
    Returns:
        str: 编码后的 JWT 访问令牌字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """解码访问令牌
    
    验证并解码 JWT 访问令牌，提取其中的数据。
    如果令牌无效或过期，返回 None。
    
    Args:
        token: JWT 访问令牌字符串
    
    Returns:
        Optional[dict]: 令牌中的数据（payload），无效时返回 None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
