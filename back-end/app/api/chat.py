from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import User, ChatLog
from app.schemas.chat import ChatCreate, ChatResponse, ChatList

router = APIRouter()

@router.post("/send", response_model=ChatResponse)
def send_message(*, db: Session = Depends(deps.get_db), chat_in: ChatCreate, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """发送聊天消息并获取回复"""
    # 在实际应用中，这里可能会调用AI服务来生成回复
    # 目前使用简单的回复机制作为示例
    response_text = f"这是对'{chat_in.message}'的自动回复"
    
    # 创建聊天记录
    chat_log = ChatLog(
        user_id=current_user.id,
        message=chat_in.message,
        response=response_text
    )
    
    db.add(chat_log)
    db.commit()
    db.refresh(chat_log)
    
    return chat_log

@router.get("/history", response_model=List[ChatResponse])
def get_chat_history(*, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_active_user), skip: int = 0, limit: int = 100) -> Any:
    """获取用户的聊天历史记录"""
    chat_logs = db.query(ChatLog).filter(ChatLog.user_id == current_user.id).order_by(ChatLog.timestamp.desc()).offset(skip).limit(limit).all()
    return chat_logs

@router.get("/history/{chat_id}", response_model=ChatResponse)
def get_chat_detail(*, db: Session = Depends(deps.get_db), chat_id: int, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """获取特定聊天记录的详细信息"""
    chat_log = db.query(ChatLog).filter(ChatLog.id == chat_id, ChatLog.user_id == current_user.id).first()
    if not chat_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="聊天记录不存在或无权访问"
        )
    return chat_log

@router.delete("/history/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(*, db: Session = Depends(deps.get_db), chat_id: int, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """删除特定的聊天记录"""
    chat_log = db.query(ChatLog).filter(ChatLog.id == chat_id, ChatLog.user_id == current_user.id).first()
    if not chat_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="聊天记录不存在或无权访问"
        )
    
    db.delete(chat_log)
    db.commit()
    
    return None