from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类
    
    使用 Pydantic BaseSettings 来管理所有应用配置，
    支持从环境变量和 .env 文件加载配置。
    """
    # 应用基本信息
    APP_NAME: str = "拜年助手"
    APP_VERSION: str = "1.0.0"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./newyear_greeting.db"
    
    # JWT 认证相关配置
    SECRET_KEY: str = "your-secret-key-change-in-production"  # 生产环境必须修改
    ALGORITHM: str = "HS256"  # JWT 加密算法
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 访问令牌过期时间（7天）
    
    # Redis 缓存配置
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # 用户请求限制配置
    FREE_USER_DAILY_LIMIT: int = 50  # 免费用户每日请求限制
    VIP_USER_DAILY_LIMIT: int = -1  # VIP用户每日请求限制（-1表示无限制）
    
    # CORS 跨域配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:5174", "http://localhost:8080"]
    
    class Config:
        """配置类
        
        指定环境变量文件的位置。
        """
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """获取应用配置的单例函数
    
    使用 lru_cache 装饰器确保配置只被加载一次，
    避免重复读取环境变量和配置文件。
    
    Returns:
        Settings: 应用配置实例
    """
    return Settings()


settings = get_settings()
