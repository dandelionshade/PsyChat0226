from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    role: str = Field(default="user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    navigations: List["Navigation"] = Relationship(back_populates="creator")
    chat_logs: List["ChatLog"] = Relationship(back_populates="user")
    logs: List["Log"] = Relationship(back_populates="user")
    recommendations: List["Recommendation"] = Relationship(back_populates="user")

class Navigation(SQLModel, table=True):
    __tablename__ = "navigation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # 关系
    creator: Optional[User] = Relationship(back_populates="navigations")
    recommendations: List["Recommendation"] = Relationship(back_populates="content")

class ChatLog(SQLModel, table=True):
    __tablename__ = "chat_logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    message: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    user: Optional[User] = Relationship(back_populates="chat_logs")

class Log(SQLModel, table=True):
    __tablename__ = "logs"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    action: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    user: Optional[User] = Relationship(back_populates="logs")

class Recommendation(SQLModel, table=True):
    __tablename__ = "recommendations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    content_id: int = Field(foreign_key="navigation.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # 关系
    user: Optional[User] = Relationship(back_populates="recommendations")
    content: Optional[Navigation] = Relationship(back_populates="recommendations")