from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..core.deps import get_current_active_user
from ..core.deps_anonymous import get_anonymous_or_user
from ..models.user import User
from ..schemas.conversation import (
    ConversationCreate, ConversationUpdate, ConversationResponse,
    MessageCreate, MessageResponse, ChatRequest
)
from ..services.conversation_service import ConversationService

router = APIRouter(prefix="/api/conversations", tags=["对话"])


@router.post("", response_model=ConversationResponse)
async def create_conversation(
    conv_data: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """创建新对话
    
    为当前登录用户创建一个新的对话会话。
    
    Args:
        conv_data: 对话创建数据（标题等）
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        ConversationResponse: 创建的对话信息
    """
    service = ConversationService(db)
    conv = service.create_conversation(current_user.id, conv_data)
    return ConversationResponse.model_validate(conv)


@router.get("", response_model=List[ConversationResponse])
async def get_conversations(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户的对话列表
    
    返回当前登录用户的所有对话，支持分页。
    
    Args:
        skip: 跳过的记录数（用于分页）
        limit: 返回的最大记录数
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        List[ConversationResponse]: 对话列表
    """
    service = ConversationService(db)
    conversations = service.get_user_conversations(current_user.id, skip, limit)
    return [ConversationResponse.model_validate(c) for c in conversations]


@router.get("/{conv_id}", response_model=ConversationResponse)
async def get_conversation(
    conv_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取单个对话详情
    
    根据对话 ID 获取对话的完整信息，包括所有消息。
    
    Args:
        conv_id: 对话 ID
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        ConversationResponse: 对话详细信息
    
    Raises:
        HTTPException: 对话不存在时抛出 404 异常
    """
    service = ConversationService(db)
    conv = service.get_conversation(conv_id, current_user.id)
    if not conv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="对话不存在")
    return ConversationResponse.model_validate(conv)


@router.put("/{conv_id}", response_model=ConversationResponse)
async def update_conversation(
    conv_id: int,
    conv_data: ConversationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """更新对话信息
    
    更新对话的标题或其他可修改信息。
    
    Args:
        conv_id: 对话 ID
        conv_data: 要更新的对话数据
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        ConversationResponse: 更新后的对话信息
    
    Raises:
        HTTPException: 对话不存在时抛出 404 异常
    """
    service = ConversationService(db)
    conv = service.update_conversation(conv_id, current_user.id, conv_data)
    if not conv:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="对话不存在")
    return ConversationResponse.model_validate(conv)


@router.delete("/{conv_id}")
async def delete_conversation(
    conv_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """删除对话
    
    删除指定 ID 的对话及其所有消息。
    
    Args:
        conv_id: 对话 ID
        current_user: 当前登录用户
        db: 数据库会话
    
    Returns:
        dict: 删除成功消息
    
    Raises:
        HTTPException: 对话不存在时抛出 404 异常
    """
    service = ConversationService(db)
    success = service.delete_conversation(conv_id, current_user.id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="对话不存在")
    return {"message": "删除成功"}


@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_anonymous_or_user),
    db: Session = Depends(get_db)
):
    """发送消息并获取 AI 回复
    
    发送用户消息到对话中，获取 AI 的回复。
    支持匿名用户使用此接口。
    
    Args:
        request: 聊天请求，包含消息内容和可选的对话 ID
        current_user: 当前用户（登录用户或匿名用户）
        db: 数据库会话
    
    Returns:
        dict: 包含对话和 AI 消息的响应
    """
    service = ConversationService(db)
    conv, ai_msg = await service.chat(
        current_user.id,
        request.message,
        request.conversation_id
    )
    
    return {
        "conversation": ConversationResponse.model_validate(conv),
        "message": MessageResponse.model_validate(ai_msg)
    }
