from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.models import User, Navigation
from app.schemas.navigation import NavigationCreate, NavigationResponse, NavigationUpdate

router = APIRouter()

@router.post("/", response_model=NavigationResponse)
def create_navigation(*, db: Session = Depends(deps.get_db), navigation_in: NavigationCreate, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """创建导航内容"""
    navigation = Navigation(
        title=navigation_in.title,
        description=navigation_in.description,
        url=navigation_in.url,
        created_by=current_user.id
    )
    
    db.add(navigation)
    db.commit()
    db.refresh(navigation)
    
    return navigation

@router.get("/", response_model=List[NavigationResponse])
def get_navigations(*, db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    """获取所有导航内容"""
    navigations = db.query(Navigation).offset(skip).limit(limit).all()
    return navigations

@router.get("/{navigation_id}", response_model=NavigationResponse)
def get_navigation(*, db: Session = Depends(deps.get_db), navigation_id: int) -> Any:
    """获取特定导航内容的详细信息"""
    navigation = db.query(Navigation).filter(Navigation.id == navigation_id).first()
    if not navigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="导航内容不存在"
        )
    return navigation

@router.put("/{navigation_id}", response_model=NavigationResponse)
def update_navigation(*, db: Session = Depends(deps.get_db), navigation_id: int, navigation_in: NavigationUpdate, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """更新导航内容"""
    navigation = db.query(Navigation).filter(Navigation.id == navigation_id).first()
    if not navigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="导航内容不存在"
        )
    
    # 检查权限（只有创建者或管理员可以更新）
    if navigation.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    # 更新字段
    if navigation_in.title is not None:
        navigation.title = navigation_in.title
    if navigation_in.description is not None:
        navigation.description = navigation_in.description
    if navigation_in.url is not None:
        navigation.url = navigation_in.url
    
    db.add(navigation)
    db.commit()
    db.refresh(navigation)
    
    return navigation

@router.delete("/{navigation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_navigation(*, db: Session = Depends(deps.get_db), navigation_id: int, current_user: User = Depends(deps.get_current_active_user)) -> Any:
    """删除导航内容"""
    navigation = db.query(Navigation).filter(Navigation.id == navigation_id).first()
    if not navigation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="导航内容不存在"
        )
    
    # 检查权限（只有创建者或管理员可以删除）
    if navigation.created_by != current_user.id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    
    db.delete(navigation)
    db.commit()
    
    return None