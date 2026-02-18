from typing import List, Optional
from sqlalchemy.orm import Session
from ..models.greeting import Greeting, UserGreeting, TargetGroup, StyleType, FormatType
from ..schemas.greeting import GreetingCreate, GreetingGenerateRequest, GreetingOptimizeRequest
from .ai_service import ai_service
from .greeting_templates import get_greeting_template, add_keywords_to_greeting
import random


class GreetingService:
    """祝福语服务类
    
    负责管理祝福语的生成、优化、查询和收藏等功能。
    支持多种风格、格式和目标人群的祝福语生成。
    """
    
    def __init__(self, db: Session):
        """初始化祝福语服务
        
        Args:
            db: SQLAlchemy 数据库会话
        """
        self.db = db
    
    def get_greetings(
        self,
        target_group: Optional[TargetGroup] = None,
        style: Optional[StyleType] = None,
        format_type: Optional[FormatType] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[Greeting]:
        """获取祝福语列表
        
        根据筛选条件获取祝福语列表，支持分页。
        
        Args:
            target_group: 目标群体筛选
            style: 风格筛选
            format_type: 格式类型筛选
            skip: 跳过的记录数（分页用）
            limit: 返回的最大记录数
        
        Returns:
            List[Greeting]: 祝福语列表
        """
        query = self.db.query(Greeting)
        
        if target_group:
            query = query.filter(Greeting.target_group == target_group)
        if style:
            query = query.filter(Greeting.style == style)
        if format_type:
            query = query.filter(Greeting.format_type == format_type)
        
        return query.offset(skip).limit(limit).all()
    
    async def generate_greeting(self, request: GreetingGenerateRequest, user_id: int) -> List[str]:
        """生成祝福语
        
        根据用户请求生成指定数量和要求的祝福语。
        使用模板和关键词组合生成。
        
        Args:
            request: 生成请求，包含目标群体、风格、格式等
            user_id: 用户 ID
        
        Returns:
            List[str]: 生成的祝福语列表
        """
        target_group_str = request.target_group.value
        style_str = request.style.value
        format_type_str = request.format_type.value
        
        templates = get_greeting_template(target_group_str, style_str, format_type_str)
        
        if not templates:
            templates = get_greeting_template("general", "formal", format_type_str)
        
        greetings = []
        
        selected_templates = random.sample(templates, min(len(templates), request.count))
        
        for template in selected_templates:
            if request.keywords:
                greeting = add_keywords_to_greeting(template, request.keywords)
            else:
                greeting = template
            
            greetings.append(greeting)
            
            greeting_obj = Greeting(
                content=greeting,
                target_group=request.target_group,
                style=request.style,
                format_type=request.format_type,
                zodiac_year="2026"
            )
            self.db.add(greeting_obj)
        
        self.db.commit()
        
        return greetings
    
    async def optimize_greeting(
        self, 
        request: GreetingOptimizeRequest
    ) -> dict:
        """优化祝福语
        
        使用 AI 优化用户提供的祝福语，可选择提供替代方案。
        
        Args:
            request: 优化请求，包含原始内容和优化要求
        
        Returns:
            dict: 包含原始内容、优化内容和可选的替代方案
        """
        optimized = await ai_service.optimize_text(
            content=request.content,
            target_style=request.target_style.value if request.target_style else None,
            target_group=request.target_group.value if request.target_group else None,
            length_adjust=request.length_adjust
        )
        
        result = {
            "original": request.content,
            "optimized": optimized
        }
        
        if request.avoid_duplicate:
            alternatives = await ai_service.generate_greeting(
                target_group=request.target_group.value if request.target_group else "general",
                style=request.target_style.value if request.target_style else "formal",
                format_type="sentence",
                count=2
            )
            result["alternatives"] = alternatives
        
        return result
    
    async def custom_greeting(self, recipient_info: str, relationship: str, style: StyleType) -> str:
        """生成定制祝福语
        
        根据收件人信息、关系和风格生成个性化的祝福语。
        
        Args:
            recipient_info: 收件人信息
            relationship: 关系描述
            style: 风格类型
        
        Returns:
            str: 定制的祝福语
        """
        prompt = f"""
        请为以下对象生成一条专属拜年祝福：
        
        接收者信息：{recipient_info}
        关系：{relationship}
        风格：{style.value}
        
        要求：
        - 贴合2026丙午马年
        - 根据关系和接收者信息个性化定制
        - 温馨得体，避免生硬
        """
        
        return await ai_service.chat_completion([{"role": "user", "content": prompt}])
    
    def save_greeting(self, user_id: int, greeting_id: int) -> bool:
        """收藏祝福语
        
        将指定的祝福语添加到用户的收藏列表。
        
        Args:
            user_id: 用户 ID
            greeting_id: 祝福语 ID
        
        Returns:
            bool: 收藏成功返回 True，祝福语不存在返回 False
        """
        greeting = self.db.query(Greeting).filter(Greeting.id == greeting_id).first()
        if not greeting:
            return False
        
        existing = self.db.query(UserGreeting).filter(
            UserGreeting.user_id == user_id,
            UserGreeting.greeting_id == greeting_id
        ).first()
        
        if existing:
            return True
        
        user_greeting = UserGreeting(
            user_id=user_id,
            greeting_id=greeting_id
        )
        self.db.add(user_greeting)
        self.db.commit()
        return True


def get_greeting_service(db: Session) -> GreetingService:
    """获取祝福语服务实例
    
    Args:
        db: 数据库会话
    
    Returns:
        GreetingService: 祝福语服务实例
    """
    return GreetingService(db)
