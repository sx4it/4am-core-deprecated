from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import Base

class UserKey(Base):
    __tablename__ = 'userkey'

    id = Column(Integer, primary_key=True)
    name = Column(String(55), nullable=False)
    key = Column(String(2048), nullable=False)
    type = Column(String(255), nullable=False)
    detail = Column(String(255), nullable=True)

    # @ManyToOne : UserKey <--> User
    user_id = Column(String(255), ForeignKey('user.login'))
    user = relationship("User", backref="userkey")

    def __init__(self, name, key, type=None, detail=None):
        self.name = name
        self.key = key
        self.type = type
        self.detail = detail
