from typing import List

from sqlalchemy import String, Integer, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Seller(BaseModel):
    __tablename__ = "seller_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    books_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer), nullable=False)
