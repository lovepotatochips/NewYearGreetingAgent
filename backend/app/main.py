from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api import auth, conversation, greeting, tool

# 创建 FastAPI 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="拜年助手 - AI智能春节祝福助手"
)

# 配置 CORS 中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册各个功能模块的路由
app.include_router(auth.router)
app.include_router(conversation.router)
app.include_router(greeting.router)
app.include_router(tool.router)


# 应用启动事件：创建数据库表
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


# 根路由：返回API基本信息
@app.get("/")
async def root():
    return {
        "message": "拜年助手 API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


# 健康检查路由：用于监控服务状态
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# 直接运行应用：启动开发服务器
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
