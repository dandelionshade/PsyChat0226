from typing import Optional, List
from pydantic import BaseModel, HttpUrl


class NavigationBase(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None


class NavigationCreate(NavigationBase):
    pass


class NavigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None


class NavigationResponse(NavigationBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True


class NavigationList(BaseModel):
    navigations: List[NavigationResponse]
    total: int