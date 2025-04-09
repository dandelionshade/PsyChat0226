from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas
from app.core import security
from app.core.config import settings
from app.models.models import User
from app.api import deps

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(*, db: Session = Depends(deps.get_db), user_in: schemas.UserCreate) -> Any:
    """用户注册"""
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册"
        )
    
    user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=security.get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(*, db: Session = Depends(deps.get_db), user_in: schemas.UserLogin) -> Any:
    """用户登录"""
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not security.verify_password(user_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/me", response_model=schemas.UserResponse)
def update_user_me(*, db: Session = Depends(deps.get_db), current_user: User = Depends(deps.get_current_user), user_in: schemas.UserUpdate) -> Any:
    """更新当前用户信息"""
    if user_in.email is not None:
        current_user.email = user_in.email
    if user_in.username is not None:
        current_user.username = user_in.username
    if user_in.password is not None:
        current_user.password_hash = security.get_password_hash(user_in.password)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/me", response_model=schemas.UserResponse)
def read_user_me(current_user: User = Depends(deps.get_current_user)) -> Any:
    """获取当前用户信息"""
    return current_user