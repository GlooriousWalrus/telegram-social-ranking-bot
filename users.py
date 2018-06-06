from sqlalchemy import Column, Integer

from base import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegramid = Column(Integer, nullable=False, unique=True)
    score = Column(Integer, nullable=False)

    def __init__(self, telegramid, score):
        self.telegramid = telegramid
        self.score = score
