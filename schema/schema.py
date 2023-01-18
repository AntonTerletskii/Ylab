from typing import Optional

from pydantic import BaseModel


class Menu(BaseModel):
    id: Optional[int]
    title: str
    description: str

    class Config:
        orm_mode = True


class SubMenu(BaseModel):
    id: Optional[int]
    title: str
    description: str
    menu_id: Optional[int]

    class Config:
        orm_mode = True


class Dishes(BaseModel):
    id: Optional[int]
    title: str
    description: str
    price: float
    sub_menu_id: Optional[int]

    class Config:
        orm_mode = True
