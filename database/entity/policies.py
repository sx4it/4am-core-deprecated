#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Policies(Base):
    __tablename__ = 'policies'

    id = Column(Integer, primary_key=True)
    polname = Column(String(255), nullable=False)
    allert = Column(Boolean, nullable=False)

    # OneToOne : Host --> Policies
    # /

    # OneToOne : HostGroup --> Policies
    # /

    def __init__(self, polname, allert):
        self.polname = polname
        self.allert = allert
