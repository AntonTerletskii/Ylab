import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from model.Yentities import Menu as ModelMenu
from model.Yentities import SubMenu as ModelSubMenu
from model.Yentities import Dishes as ModelDishes
from schema.schema import Menu as SchemaMenu
from schema.schema import SubMenu as SchemaSubMenu
from schema.schema import Dishes as SchemaDishes

# Загрузка переменных окружения из файла .env
load_dotenv('.env')
# Создаём экземпляр объекта FastAPI
app = FastAPI()
# Инициализиурем экземпляр объекта FastAPI
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])


# BEGIN
# Создаём методы RestAPI

# CRUD меню
@app.get('/api/v1/menus')
def get_all_menus():
    """Просматривает список меню"""
    menus = db.session.query(ModelMenu).all()
    return menus


@app.get("/api/v1/menus/{target_menu_id}")
def get_one_menu(target_menu_id: int):
    """Просматривает определенное меню"""
    one_menu = db.session.query(ModelMenu).get(target_menu_id)
    return one_menu


@app.post('/api/v1/menus', response_model=SchemaMenu)
def create_menu(menu: SchemaMenu):
    """Создает меню"""
    db_menu = ModelMenu(title=menu.title, description=menu.description)
    db.session.add(db_menu)
    db.session.commit()
    return db_menu


@app.patch("/api/v1/menus/{target_menu_id}", response_model=SchemaMenu)
def update_menu(menu: SchemaMenu, target_menu_id: int):
    """Обновляет определенное меню с идентификатором равным target_menu_id"""
    db_menu_query = db.session.query(ModelMenu).filter(ModelMenu.id == target_menu_id)
    if db_menu_query is not None:
        db_menu_query.update({'title': menu.title, 'description': menu.description}, synchronize_session='evaluate')
        db.session.commit()
    return db.session.query(ModelMenu).get(target_menu_id)


@app.delete("/api/v1/menus/{target_menu_id}")
def delete_menu(target_menu_id: int):
    """Удаляет определенное меню"""
    db_menu_query = db.session.query(ModelMenu).filter(ModelMenu.id == target_menu_id)
    db_menu_query.delete(synchronize_session='evaluate')
    db.session.commit()


# CRUD подменю
@app.get("/api/v1/menus/{target_menu_id}/submenus")
def get_all_sub_menus(target_menu_id: int):
    """Просматривает список подменю строго определенного меню, задаваемого идентификатором target_menu_id"""
    sub_menus = db.session.query(ModelSubMenu).filter(ModelSubMenu.menu_id == target_menu_id).all()
    return sub_menus


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def get_one_sub_menu(target_menu_id: int, target_submenu_id: int):
    """Просматривает определенное подменю"""
    one_sub_menu = db.session.query(ModelSubMenu).filter(ModelSubMenu.menu_id == target_menu_id, ModelSubMenu.id ==
                                                         target_submenu_id).one_or_none()
    return one_sub_menu


@app.post('/api/v1/menus/{target_menu_id}/submenus', response_model=SchemaSubMenu)
def create_sub_menu(sub_menu: SchemaSubMenu, target_menu_id: int):
    """Создает подменю"""
    db_sub_menu = ModelSubMenu(title=sub_menu.title, description=sub_menu.description, menu_id=target_menu_id)
    db.session.add(db_sub_menu)
    db.session.commit()
    return db_sub_menu


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}", response_model=SchemaSubMenu)
def update_sub_menu(sub_menu: SchemaMenu, target_menu_id: int, target_submenu_id: int):
    """Обновляет определенное подменю с идентификатором равным target_menu_id"""
    db_sub_menu_query = db.session.query(ModelSubMenu).filter(ModelSubMenu.menu_id == target_menu_id, ModelSubMenu.id ==
                                                              target_submenu_id)
    if db_sub_menu_query is not None:
        db_sub_menu_query.update({'title': sub_menu.title, 'description': sub_menu.description},
                                 synchronize_session='evaluate')
        db.session.commit()
    return db.session.query(ModelSubMenu).get(target_submenu_id)


@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
def delete_sub_menu(target_menu_id: int, target_submenu_id: int):
    """Удаляет определенное подменю"""
    # Удаляем блюда, которые привязаны к подменю задаваемому id = target_submenu_id
    db_dish_query = db.session.query(ModelDishes).filter(ModelDishes.sub_menu_id == target_submenu_id)
    db_dish_query.delete(synchronize_session='evaluate')
    # Удаляем определенное подменю задавемое id = target_sub_menu
    db_sub_menu_query = db.session.query(ModelSubMenu).filter(ModelSubMenu.menu_id == target_menu_id, ModelSubMenu.id ==
                                                              target_submenu_id)
    db_sub_menu_query.delete(synchronize_session='evaluate')
    db.session.commit()


# CRUD блюда
@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes")
def get_all_dishes(target_menu_id: int, target_submenu_id: int):
    """Просматривает список блюд"""
    sub_dishes = db.session.query(ModelDishes).filter(ModelDishes.sub_menu_id == target_submenu_id).all()
    return sub_dishes


@app.get("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def get_one_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    """Просматривает определенное блюдо"""
    dish = db.session.query(ModelDishes).get(target_dish_id)
    return dish


@app.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', response_model=SchemaDishes)
def create_dishes(dish: SchemaDishes, target_menu_id: int, target_submenu_id: int):
    """Создает блюдо"""
    db_dishes = ModelDishes(title=dish.title, description=dish.description, price=dish.price,
                            sub_menu_id=target_submenu_id)
    db.session.add(db_dishes)
    db.session.commit()
    return db_dishes


@app.patch("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}",
           response_model=SchemaDishes)
def update_dishes(dishes: SchemaDishes, target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    """Обновляет определенное блюдо с идентификатором равным target_menu_id"""
    db_dishes = db.session.query(ModelDishes).filter(ModelDishes.sub_menu_id == target_submenu_id, ModelDishes.id ==
                                                     target_dish_id)
    if db_dishes is not None:
        db_dishes.update({'title': dishes.title, 'description': dishes.description, 'price': dishes.price},
                         synchronize_session='evaluate')
        db.session.commit()
    return db.session.query(ModelDishes).get(target_dish_id)


@app.delete("/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
def delete_dish(target_menu_id: int, target_submenu_id: int, target_dish_id: int):
    """Удаляет определенное блюдо"""
    db_dish_query = db.session.query(ModelDishes).filter(ModelDishes.sub_menu_id == target_submenu_id, ModelDishes.id ==
                                                   target_dish_id)
    db_dish_query.delete(synchronize_session='evaluate')
    db.session.commit()


#
#
# # END
# @app.post('/sub_menu/', response_model=SchemaSubMenu)
# async def sub_menu(sub_menu: SchemaSubmenu):
#     db_sub_menu = ModelSubMenu(name=sub_menu.name, dishes=sub_menu.dishes)
#     db.session.add(db_sub_menu)
#     db.session.commit()
#     return sub_menu
#
#
# @app.get('/sub_menu/')
# async def sub_menu():
#     sub_menu = db.session.query(ModelSubMenu).all()
#     return sub_menu
#
#
# @app.post('/dishes/', response_model=SchemaDishes)
# async def dishes(dishes: SchemaDishes):
#     db_dishes = ModelDishes(name=sub_menu.name, dishes=sub_menu.dishes)
#     db.session.add(db_sub_menu)
#     db.session.commit()
#     return sub_menu
#
#
# @app.get('/sub_menu/')
# async def sub_menu():
#     sub_menu = db.session.query(ModelSubMenu).all()
#     return sub_menu
#
#
# # To run locally
# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)

def main():
    uvicorn.run(app, host='0.0.0.0', port=8000)


if __name__ == '__main__':
    main()
