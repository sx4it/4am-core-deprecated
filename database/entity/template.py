#!/usr/bin/env python

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, backref

from base import Base

class Template(Base):
    __tablename__ = 'template'

    id = Column(Integer, primary_key=True)
    tpname = Column(String(255), nullable=False)
    sshd_conf_path = Column(String(255))
    sshd_version = Column(BigInteger)

    # OneToOne : Host --> Template
    # /

    def __init__(self, tpname, sshd_conf_path, sshd_version):
        self.tpname = tpname
        self.sshd_conf_path = sshd_conf_path
        self.sshd_version = sshd_version
