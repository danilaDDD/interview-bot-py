from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import AbsId


class Account(AbsId):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, unique=True, nullable=False)
    email = Column(String(100), nullable=False)
    username = Column(String(100))
    first_name = Column(String(50))
    last_name = Column(String(50))