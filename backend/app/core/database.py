from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """数据库会话依赖函数
    
    为 FastAPI 路由提供数据库会话的依赖注入。
    使用 yield 确保请求结束后会话被正确关闭。
    
    Yields:
        Session: SQLAlchemy 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
