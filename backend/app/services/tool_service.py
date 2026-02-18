from typing import List, Dict
from sqlalchemy.orm import Session
from ..models.tool import Custom, Etiquette, GiftSuggestion
from .tool_templates import (
    get_custom_answer,
    get_etiquette_guidance,
    get_gift_suggestions,
    get_red_packet_recommendations,
    get_menu_suggestions,
    get_schedule_suggestions,
    format_gift_suggestions,
    format_red_packet_recommendations,
    format_menu_suggestions
)


class ToolService:
    """工具服务类
    
    负责提供各种春节实用工具的服务，包括：
    - 习俗查询
    - 礼仪指导
    - 礼物推荐
    - 红包建议
    - 年夜饭菜单推荐
    - 春节行程安排
    """
    
    def __init__(self, db: Session):
        """初始化工具服务
        
        Args:
            db: SQLAlchemy 数据库会话
        """
        self.db = db
    
    async def query_custom(self, question: str, region: str = None) -> dict:
        """查询春节习俗
        
        根据用户问题查询相关的春节习俗知识。
        
        Args:
            question: 用户问题
            region: 可选的地区信息
        
        Returns:
            dict: 包含问题和答案的响应
        """
        answer = get_custom_answer(question, region)
        
        return {
            "question": question,
            "answer": answer
        }
    
    async def query_etiquette(self, scenario: str, category: str = None) -> dict:
        """查询拜年礼仪
        
        根据场景和类别查询拜年礼仪指导。
        
        Args:
            scenario: 场景描述
            category: 可选的类别（如朋友、长辈、领导等）
        
        Returns:
            dict: 包含场景和礼仪指导的响应
        """
        target = category if category else "朋友"
        guidance = get_etiquette_guidance(target, scenario)
        
        return {
            "scenario": scenario,
            "guidance": guidance
        }
    
    async def suggest_gift(self, target_group: str, budget: str = None, occasion: str = "new_year") -> dict:
        """推荐春节礼物
        
        根据目标群体推荐合适的春节礼物。
        
        Args:
            target_group: 目标群体（长辈、领导、朋友等）
            budget: 可选的预算
            occasion: 场合，默认为春节
        
        Returns:
            dict: 包含目标群体和礼物建议的响应
        """
        suggestions = get_gift_suggestions(target_group)
        formatted = format_gift_suggestions(suggestions)
        
        return {
            "target_group": target_group,
            "suggestions": formatted
        }
    
    async def suggest_red_packet(
        self, 
        amount_type: str, 
        relationship: str = None, 
        meaning: str = None
    ) -> dict:
        """建议红包金额
        
        根据金额类型和关系推荐合适的红包金额。
        
        Args:
            amount_type: 金额类型（如吉利数字、经典等）
            relationship: 关系类型
            meaning: 寓意
        
        Returns:
            dict: 包含金额类型和推荐金额的响应
        """
        recommendations = get_red_packet_recommendations(amount_type)
        formatted = format_red_packet_recommendations(recommendations)
        
        return {
            "amount_type": amount_type,
            "recommendations": formatted
        }
    
    async def suggest_new_year_menu(
        self, 
        people_count: int, 
        taste_preference: str = None, 
        budget: str = None
    ) -> dict:
        """推荐年夜饭菜单
        
        根据人数推荐年夜饭菜单。
        
        Args:
            people_count: 用餐人数
            taste_preference: 可选的口味偏好
            budget: 可选的预算
        
        Returns:
            dict: 包含人数和菜单建议的响应
        """
        menu = get_menu_suggestions()
        formatted = format_menu_suggestions(menu)
        
        return {
            "people_count": people_count,
            "menu_suggestions": formatted
        }
    
    async def suggest_schedule(
        self, 
        date: str, 
        region: str = None, 
        activity_type: str = None
    ) -> dict:
        """建议春节行程安排
        
        根据日期推荐春节行程安排。
        
        Args:
            date: 日期
            region: 可选的地区
            activity_type: 可选的活动类型
        
        Returns:
            dict: 包含日期和行程安排的响应
        """
        schedule = get_schedule_suggestions(date)
        
        return {
            "date": date,
            "schedule": schedule
        }


def get_tool_service(db: Session) -> ToolService:
    """获取工具服务实例
    
    Args:
        db: 数据库会话
    
    Returns:
        ToolService: 工具服务实例
    """
    return ToolService(db)
