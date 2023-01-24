from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String, Column, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
SCHEMA_NAME = 'rest_food'


class Menu(Base):
    """Сущность меню
    Если удалить меню, должны удалиться все подменю и блюда этого меню
    Во время выдачи списка меню, для кадждого меню добавлять кол-во подменю и блюд в этом меню"""
    __tablename__ = "menu"
    __table_args__ = {'schema': SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    sub_menus = relationship("SubMenu", uselist=True)

    @property
    def submenus_count(self):
        return len(self.sub_menus)

    @property
    def dishes_count(self):
        # Я зашёл в подъезд
        # Буду перебирать каждую квартиру в цикле
        sum_of_dishes = 0
        for sub_menu in self.sub_menus:
            sum_of_dishes = sum_of_dishes + len(sub_menu.dishes)
        return sum_of_dishes


class SubMenu(Base):
    """Сущность подменю
    Подменю не может находиться в двух подменю одновременно
    Если удалить подменю, должны удалиться все блюда этого подменю
    Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю"""
    __tablename__ = "sub_menu"
    __table_args__ = {'schema': SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("{}.menu.id".format(SCHEMA_NAME)))
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    dishes = relationship("Dishes", uselist=True)

    @property
    def dishes_count(self):
        return len(self.dishes)


class Dishes(Base):
    """Сущность блюда
    Блюдо не может быть привязано напрямую к меню, минуя подменю
    Блюдо не может находиться в двух подменю одновременно
    Цены блюд выводить с округлением до двух знаков после запятой"""
    __tablename__ = "dishes"
    __table_args__ = {'schema': SCHEMA_NAME}
    id = Column(Integer, primary_key=True, autoincrement=True)
    sub_menu_id = Column(Integer, ForeignKey("{}.sub_menu.id".format(SCHEMA_NAME)))
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
