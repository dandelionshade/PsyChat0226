from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class ChatBase(BaseModel):
    message: str


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    message: Optional[str] = None
    response: Optional[str] = None


class ChatResponse(ChatBase):
    id: int
    user_id: int
    response: str
    timestamp: datetime

    class Config:
        orm_mode = True


class ChatList(BaseModel):
    chats: List[ChatResponse]
    total: int