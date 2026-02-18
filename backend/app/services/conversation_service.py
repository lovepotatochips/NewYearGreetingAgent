from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.conversation import Conversation, Message
from ..schemas.conversation import ConversationCreate, ConversationUpdate, MessageCreate
from .ai_service import ai_service
from .knowledge_service import get_knowledge_service


class ConversationService:
    """对话服务类
    
    负责管理用户对话和消息的业务逻辑，包括对话的创建、查询、
    更新、删除，以及消息发送和 AI 回复生成等功能。
    """
    
    def __init__(self, db: Session):
        """初始化对话服务
        
        Args:
            db: SQLAlchemy 数据库会话
        """
        self.db = db
    
    def create_conversation(self, user_id: int, conv_data: ConversationCreate) -> Conversation:
        """创建新对话
        
        为指定用户创建一个新的对话会话。
        
        Args:
            user_id: 用户 ID
            conv_data: 对话创建数据（标题等）
        
        Returns:
            Conversation: 创建的对话对象
        """
        db_conv = Conversation(
            user_id=user_id,
            title=conv_data.title
        )
        self.db.add(db_conv)
        self.db.commit()
        self.db.refresh(db_conv)
        return db_conv
    
    def get_conversation(self, conv_id: int, user_id: int) -> Optional[Conversation]:
        """获取对话详情
        
        获取指定 ID 的对话，确保该对话属于指定用户。
        
        Args:
            conv_id: 对话 ID
            user_id: 用户 ID
        
        Returns:
            Optional[Conversation]: 对话对象，不存在或不属于该用户时返回 None
        """
        return self.db.query(Conversation).filter(
            Conversation.id == conv_id,
            Conversation.user_id == user_id
        ).first()
    
    def get_user_conversations(self, user_id: int, skip: int = 0, limit: int = 50) -> List[Conversation]:
        """获取用户的所有对话
        
        获取指定用户的所有对话，按更新时间倒序排列，支持分页。
        
        Args:
            user_id: 用户 ID
            skip: 跳过的记录数（分页用）
            limit: 返回的最大记录数
        
        Returns:
            List[Conversation]: 对话列表
        """
        return self.db.query(Conversation).filter(
            Conversation.user_id == user_id
        ).order_by(Conversation.updated_at.desc()).offset(skip).limit(limit).all()
    
    def update_conversation(
        self, 
        conv_id: int, 
        user_id: int, 
        conv_data: ConversationUpdate
    ) -> Optional[Conversation]:
        """更新对话信息
        
        更新对话的标题等信息。
        
        Args:
            conv_id: 对话 ID
            user_id: 用户 ID
            conv_data: 更新数据
        
        Returns:
            Optional[Conversation]: 更新后的对话对象
        """
        conv = self.get_conversation(conv_id, user_id)
        if conv and conv_data.title:
            conv.title = conv_data.title
            self.db.commit()
            self.db.refresh(conv)
        return conv
    
    def delete_conversation(self, conv_id: int, user_id: int) -> bool:
        """删除对话
        
        删除指定 ID 的对话及其所有消息。
        
        Args:
            conv_id: 对话 ID
            user_id: 用户 ID
        
        Returns:
            bool: 删除成功返回 True，否则返回 False
        """
        conv = self.get_conversation(conv_id, user_id)
        if conv:
            self.db.delete(conv)
            self.db.commit()
            return True
        return False
    
    def create_message(
        self, 
        conv_id: int, 
        user_id: int, 
        role: str, 
        content: str
    ) -> Message:
        """创建消息
        
        在指定对话中创建一条新消息，并更新对话的更新时间。
        
        Args:
            conv_id: 对话 ID
            user_id: 用户 ID
            role: 消息角色（user/assistant）
            content: 消息内容
        
        Returns:
            Message: 创建的消息对象
        """
        db_msg = Message(
            conversation_id=conv_id,
            user_id=user_id,
            role=role,
            content=content
        )
        self.db.add(db_msg)
        
        conv = self.db.query(Conversation).filter(Conversation.id == conv_id).first()
        if conv:
            conv.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(db_msg)
        return db_msg
    
    async def chat(self, user_id: int, message: str, conversation_id: Optional[int] = None) -> tuple:
        """处理聊天请求
        
        接收用户消息，生成 AI 回复，并保存到对话中。
        首先尝试从知识库中查找匹配的答案，如果没有匹配则调用 AI 生成回复。
        
        Args:
            user_id: 用户 ID
            message: 用户消息内容
            conversation_id: 对话 ID，如果为 None 则创建新对话
        
        Returns:
            tuple: (对话对象, AI 消息对象)
        """
        if conversation_id:
            conv = self.get_conversation(conversation_id, user_id)
            if not conv:
                conv = self.create_conversation(user_id, ConversationCreate())
        else:
            conv = self.create_conversation(user_id, ConversationCreate())
        
        user_msg = self.create_message(conv.id, user_id, "user", message)
        
        knowledge_service = get_knowledge_service(self.db)
        results = knowledge_service.search_with_similarity(message, threshold=0.2)
        
        if results and results[0][1] > 0.4:
            best_match = results[0][0]
            ai_response = best_match.answer
        else:
            history = self.db.query(Message).filter(
                Message.conversation_id == conv.id
            ).order_by(Message.created_at.asc()).limit(10).all()
            
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in history
            ]
            
            system_prompt = """你是拜年助手，一个专注于春节拜年的AI助手。
你的主要功能包括：
1. 生成各种拜年祝福文案（按人群、风格、格式分类）
2. 优化和改写用户提供的文案
3. 解答春节习俗和礼仪问题
4. 提供送礼建议、红包建议
5. 推荐年夜饭菜单
6. 提供春节安排建议

回答要简洁、实用、贴合春节氛围。如果用户需求模糊，请主动追问。
"""
            
            ai_response = await ai_service.chat_completion(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=800
            )
        
        ai_msg = self.create_message(conv.id, user_id, "assistant", ai_response)
        
        return conv, ai_msg


def get_conversation_service(db: Session) -> ConversationService:
    """获取对话服务实例
    
    Args:
        db: 数据库会话
    
    Returns:
        ConversationService: 对话服务实例
    """
    return ConversationService(db)
