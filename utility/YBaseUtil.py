from sqlalchemy.orm import Session
from sqlalchemy import inspect
# Постоянная(const) переменная SPECSYMBOLS, содержащая специальные символы, использующеся для проверки
# на их наличие в переменных checkLogin и check_location
SPECSYMBOLS = '$@#%^&*()=+\'\"`[]~;:,.?!§№- '


class BaseUtil:
    """Базовый класс для всех утилит"""

    def check_session_type(self, session: Session) -> None:
        if not isinstance(session, Session):
            raise Exception('Параметр session не является типом Session')

    def object_as_dict(self, obj):
        return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

