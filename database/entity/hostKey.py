#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import Base

class HostKey(Base):
    __tablename__ = 'hostkey'

    id = Column(Integer, primary_key=True)
    hkkey = Column(String(2048))
    hktype = Column(String(255))

    #ManyToOne : HostKey <--> Host
    host_id = Column(Integer, ForeignKey('host.id'))
    host = relationship("Host", backref="hostkey")

    def __init__(self, hkkey, hktype):
        self.hkkey = hkkey
        self.hktype = hktype


