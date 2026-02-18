from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..core.deps_anonymous import get_anonymous_or_user
from ..models.user import User
from ..schemas.tool import (
    CustomQueryRequest, CustomResponse,
    EtiquetteQueryRequest, EtiquetteResponse,
    GiftSuggestionRequest, GiftSuggestionResponse,
    RedPacketRequest, RedPacketResponse,
    NewYearMenuRequest, NewYearMenuResponse,
    ScheduleRequest, ScheduleResponse
)
from ..services.tool_service import ToolService

router = APIRouter(prefix="/api/tools", tags=["工具"])


@router.post("/custom")
async def query_custom(
    request: CustomQueryRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """查询春节习俗
    
    根据用户问题查询相关的春节习俗和传统知识。
    支持匿名用户使用。
    
    Args:
        request: 查询请求，包含问题内容和可选的地区信息
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含习俗解答的响应
    """
    service = ToolService(db)
    result = await service.query_custom(request.question, request.region)
    return result


@router.post("/etiquette")
async def query_etiquette(
    request: EtiquetteQueryRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """查询拜年礼仪
    
    根据场景和类别查询拜年相关的礼仪规范和注意事项。
    支持匿名用户使用。
    
    Args:
        request: 查询请求，包含场景和类别
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含礼仪指导的响应
    """
    service = ToolService(db)
    result = await service.query_etiquette(request.scenario, request.category)
    return result


@router.post("/gift")
async def suggest_gift(
    request: GiftSuggestionRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """建议春节礼物
    
    根据目标群体、预算和场合推荐合适的春节礼物。
    支持匿名用户使用。
    
    Args:
        request: 请求，包含目标群体、预算和场合
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含礼物建议的响应
    """
    service = ToolService(db)
    result = await service.suggest_gift(
        request.target_group,
        request.budget,
        request.occasion
    )
    return result


@router.post("/redpacket")
async def suggest_red_packet(
    request: RedPacketRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """建议红包金额
    
    根据金额类型、关系和寓意推荐合适的红包金额。
    支持匿名用户使用。
    
    Args:
        request: 请求，包含金额类型、关系和寓意
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含红包金额建议的响应
    """
    service = ToolService(db)
    result = await service.suggest_red_packet(
        request.amount_type,
        request.relationship,
        request.meaning
    )
    return result


@router.post("/menu")
async def suggest_new_year_menu(
    request: NewYearMenuRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """建议年夜饭菜单
    
    根据人数、口味偏好和预算推荐年夜饭菜单。
    支持匿名用户使用。
    
    Args:
        request: 请求，包含人数、口味偏好和预算
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含菜单建议的响应
    """
    service = ToolService(db)
    result = await service.suggest_new_year_menu(
        request.people_count,
        request.taste_preference,
        request.budget
    )
    return result


@router.post("/schedule")
async def suggest_schedule(
    request: ScheduleRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """建议春节行程安排
    
    根据日期、地区和活动类型推荐春节行程安排。
    支持匿名用户使用。
    
    Args:
        request: 请求，包含日期、地区和活动类型
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含行程安排建议的响应
    """
    service = ToolService(db)
    result = await service.suggest_schedule(
        request.date,
        request.region,
        request.activity_type
    )
    return result
