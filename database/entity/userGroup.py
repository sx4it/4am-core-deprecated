#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

class UserGroup(Base):
    __tablename__ = 'usergroup'

    id = Column(Integer, primary_key=True)
    ugname = Column(String(255), nullable=False)
    description = Column(String(255))

    # ManyToMany User <--> UserGroup
    # /

    # @ManyToMany :  UserGroup <--> HostGroup/Rights
    hostgroup = relationship("UserGroup_Has_HostGroup_With_Rights", backref="usergroup")

    # @ManyToMany :  UserGroup <--> Host/Rights
    host = relationship("UserGroup_Has_Host_With_Rights", backref="usergroup")

    def __init__(self, ugname, description):
        self.ugname = ugname
        self.description = description
