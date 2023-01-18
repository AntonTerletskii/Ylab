from utility.YBaseUtil import BaseUtil
from sqlalchemy.orm import Session
from model.Yentities import Menu


class MenuUtility(BaseUtil):

    def check_menu_type(self, menu: Menu):
        check = isinstance(menu, Menu)
        if not check:
            raise Exception('Тип параметра menu не равен типу Menu')

    def check_menu_name(self, menu_name: str):
        check = isinstance(menu_name, str) and menu_name != ''
        if not check:
            raise Exception('Параметр не соответствует str либо вводимое значение в строке пусто')

    def check_menu_id(self, menu_id: int):
        check = menu_id is not None and menu_id > 0
        if not check:
            raise Exception('Параметр menu_id равен None')

    def insert(self, session: Session, new_menu: Menu) -> Menu:

        self.check_session_type(session)
        self.check_menu_type(session, new_menu)
        self.check_menu_name(session, new_menu)
        check_id = new_menu.id is None
        if not check_id:
            raise Exception('Значение атрибута id объекта new_menu равно None')

        session.add(new_menu)
        session.commit()

        return new_menu

    def update(self, session: Session, upd_menu: Menu) -> Menu:

        self.check_menu_type(session, upd_menu)
        self.check_session_type(session)
        self.check_menu_name(session, upd_menu)

        session.query(Menu).filter(Menu.id == upd_menu.id).update(vars(upd_menu.id))
        session.flush()
        session.commit()

    def delete(self, session: Session, del_menu: Menu) -> Menu:

        self.check_menu_type(session)
        self.check_menu_type(session, del_menu)
        self.check_menu_id(del_menu)

        session.query(Menu).filter(
            Menu.id == del_menu.id).delete()
        session.flush()
        session.commit()
