from typing import Optional

from pydantic import BaseModel


class Menu(BaseModel):
    id: Optional[str]
    title: Optional[str]
    description: Optional[str]
    submenus_count: Optional[int]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class SubMenu(BaseModel):
    id: Optional[str]
    title: str
    description: str
    menu_id: Optional[int]
    dishes_count: Optional[int]

    class Config:
        orm_mode = True


class Dishes(BaseModel):
    id: Optional[str]
    title: str
    description: str
    price: Optional[str]
    sub_menu_id: Optional[int]

    class Config:
        orm_mode = True
