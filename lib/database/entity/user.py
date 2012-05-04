from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref

from database.base import Base

from associationTable import userGroup_Has_User_Table

class User(Base):
    __tablename__ = 'user'

    login = Column(String(55), primary_key=True)
    firstname = Column(String(55), nullable=False)
    lastname = Column(String(55), nullable=False)
    email = Column(String(55), nullable=False)
    password = Column(String(55), nullable=False)
    registerdate = Column(DateTime, nullable=False, default=datetime.now())
    active = Column(Boolean, nullable=False, default=True)

    # @OneToMany : UserKey <--> User
    # userkey

    # @ManyToMany : User <--> UserGroup
    usergroup = relationship("UserGroup", secondary=userGroup_Has_User_Table, backref="user")

    # @ManyToMany :  User <--> HostGroup/Rights
    hostgroup = relationship("User_Has_HostGroup_With_Rights", backref="user")

    # @ManyToMany :  User <--> Host/Rights
    host = relationship("User_Has_Host_With_Rights", backref="user")

    def __init__(self, login, firstname, lastname, email, password, active=True):
        self.login = login
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.active = active
