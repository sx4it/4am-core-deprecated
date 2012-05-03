#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import Base

class Rights(Base):
    __tablename__ = 'rights'

    id = Column(Integer, primary_key=True)
    rname = Column(String(255), nullable=False)
    accountname = Column(String(255))

    def __init__(self, rname, accountname):
        self.rname = rname
        self.accountname = accountname
