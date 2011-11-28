from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import Base

class UserKey(Base):
    __tablename__ = 'userkey'
    
    id = Column(Integer, primary_key=True)
    ukkey = Column(String(2048))
    uktype = Column(String(255))

    # @ManyToOne : UserKey <--> User
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref="userkey")
    
    def __init__(self, ukkey, uktype):
        self.ukkey = ukkey
        self.uktype = uktype
        
