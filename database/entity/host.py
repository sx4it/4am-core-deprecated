#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Host(Base):
    __tablename__ = 'host'

    id = Column(Integer, primary_key=True)
    ip = Column(Integer)
    hostname = Column(String(255))
    port = Column(Integer)
    mgmtusername = Column(String(255))

    # OneToMany : HostKey <--> Host
    # /

    # OneToOne : Host --> Template
    template_id = Column(Integer, ForeignKey('template.id'))
    template = relationship("Template", backref=backref("host", uselist=False))

    # OneToOne : Host --> Policies
    policies_id = Column(Integer, ForeignKey('policies.id'))
    policies = relationship("Policies", backref=backref("host", uselist=False))

    # ManyToMany : Host <--> HostGroup
    hostgroup = relationship("HostGroup", secondary=hostGroup_Has_Host_Table, backref="host")

    def __init__(self, ip, hostname, port, mgmtusername):
        self.ip = ip
        self.hostname = hostname
        self.port = port
        self.mgmtusername = mgmtusername

