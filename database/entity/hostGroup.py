#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

class HostGroup(Base):
    __tablename__ = 'hostgroup'

    id = Column(Integer, primary_key=True)
    hgname = Column(String(255), nullable=False)
    hgdescription = Column(String(255))

    # OneToOne : HostGroup --> Policies
    policies_id = Column(Integer, ForeignKey('policies.id'))
    policies = relationship("Policies", backref=backref("hostgroup", uselist=False))

    # ManyToMany : Host <--> HostGroup
    # /

    def __init__(self, hgname, hgdescription):
        self.hgname = hgname
        self.hgdescription = hgdescription
