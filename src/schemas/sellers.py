from typing import List

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

__all__ = ["BaseSeller", "IncomingSeller", "ReturnedSeller", "ReturnedAllSellers"]


# Базовый класс "Книги", содержащий поля, которые есть во всех классах-наследниках.
class BaseSeller(BaseModel):
    first_name: str
    last_name: str
    email: str
    books_ids: List[int]


# Класс для валидации входящих данных. Не содержит id так как его присваивает БД.
class IncomingSeller(BaseSeller):
    password: str
    email: str = ""
    books_ids: List[int] = []
    # @field_validator("year")  # Валидатор, проверяет что дата не слишком древняя
    # @staticmethod
    # def validate_year(val: int):
    #     if val < 1900:
    #         raise PydanticCustomError("Validation error", "Year is wrong!")
    #     return val


# # Класс, валидирующий исходящие данные. Он уже содержит id
class ReturnedSeller(BaseSeller):
    id: int


# Класс для возврата массива объектов "Книга"
class ReturnedAllSellers(BaseModel):
    sellers: list[ReturnedSeller]
