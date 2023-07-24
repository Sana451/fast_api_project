from pydantic import BaseModel
from uuid import UUID
from decimal import Decimal


class MenuRequestCreate(BaseModel):
    title: str = "menu title"
    description: str = "menu description"


class MenuRequest(BaseModel):
    id: int
    title: str = "menu title"
    description: str = "menu description"
    submenus_count: int = 0
    dishes_count: int = 0

    class Config:
        orm_mode = True


class SubMenuRequestCreate(BaseModel):
    title: str = "submenu title"
    description: str = "submenu description"
    # menu_id: int


class SubMenuRequest(BaseModel):
    id: int
    title: str = "submenu title"
    description: str = "submenu description"
    menu_id: int
    dishes_count: int = 0

    class Config:
        orm_mode = True




class DishRequestCreate(BaseModel):
    title: str = "dish title"
    description: str = "dish description"
    price: Decimal


class DishRequest(BaseModel):
    id: int
    title: str = "dish title"
    description: str = "dish description"
    price: Decimal

    class Config:
        orm_mode = True
