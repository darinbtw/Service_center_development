from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __table__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    fio = Column(String, index=True)
    phone_number = Column(String)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, index=True)