from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_active_user, check_vip_user
from ..core.deps_anonymous import get_anonymous_or_user
from ..models.user import User
from ..schemas.greeting import (
    GreetingCreate, GreetingResponse,
    GreetingGenerateRequest, GreetingOptimizeRequest, CustomGreetingRequest
)
from ..services.greeting_service import GreetingService

router = APIRouter(prefix="/api/greetings", tags=["祝福"])


@router.get("", response_model=List[GreetingResponse])
async def get_greetings(
    target_group: str = None,
    style: str = None,
    format_type: str = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取祝福列表
    
    根据筛选条件获取祝福语列表，支持按对象群体、风格、格式类型筛选。
    
    Args:
        target_group: 对象群体（长辈、领导、朋友等）
        style: 风格类型（正式、温馨、幽默等）
        format_type: 格式类型（短句、长文、对联等）
        skip: 跳过的记录数（分页用）
        limit: 返回的最大记录数
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        List[GreetingResponse]: 祝福语列表
    """
    service = GreetingService(db)
    
    from ..models.greeting import TargetGroup, StyleType, FormatType
    
    target_group_enum = TargetGroup(target_group) if target_group else None
    style_enum = StyleType(style) if style else None
    format_type_enum = FormatType(format_type) if format_type else None
    
    greetings = service.get_greetings(target_group_enum, style_enum, format_type_enum, skip, limit)
    return [GreetingResponse.model_validate(g) for g in greetings]


@router.post("/generate")
async def generate_greeting(
    request: GreetingGenerateRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """生成祝福语
    
    根据用户指定的条件（对象、风格、格式等）生成多条祝福语。
    支持匿名用户使用。
    
    Args:
        request: 生成祝福语请求，包含目标群体、风格、格式等参数
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含生成的祝福语列表
    """
    service = GreetingService(db)
    greetings = await service.generate_greeting(request, current_user.id)
    return {"greetings": greetings}


@router.post("/optimize")
async def optimize_greeting(
    request: GreetingOptimizeRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """优化祝福语
    
    对用户提供的祝福语进行优化，使其更加精美、得体。
    支持匿名用户使用。
    
    Args:
        request: 优化请求，包含原始祝福语和优化要求
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含优化后的祝福语
    """
    service = GreetingService(db)
    result = await service.optimize_greeting(request)
    return result


@router.post("/custom")
async def custom_greeting(
    request: CustomGreetingRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """定制祝福语
    
    根据用户提供的信息（收件人信息、关系、风格）生成个性化祝福语。
    需要用户登录。
    
    Args:
        request: 定制请求，包含收件人信息和要求
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        dict: 包含定制的祝福语
    """
    service = GreetingService(db)
    greeting = await service.custom_greeting(
        request.recipient_info,
        request.relationship,
        request.style
    )
    return {"greeting": greeting}


@router.post("/{greeting_id}/save")
async def save_greeting(
    greeting_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """收藏祝福语
    
    将指定的祝福语添加到用户的收藏列表。
    
    Args:
        greeting_id: 祝福语 ID
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        dict: 收藏成功消息
    
    Raises:
        HTTPException: 祝福语不存在时抛出 404 异常
    """
    service = GreetingService(db)
    success = service.save_greeting(current_user.id, greeting_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="祝福不存在")
    return {"message": "收藏成功"}
