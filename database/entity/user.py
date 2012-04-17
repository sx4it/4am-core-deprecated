from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from database.base import Base

from associationTable import userGroup_Has_User_Table

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    firstname = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255))
    password = Column(String(255))
    registerdate = Column(DateTime, nullable=False, default=datetime.now())
    activedate  = Column(DateTime, nullable=True)
    unactivatedate = Column(DateTime, nullable=True)

    # @OneToMany : UserKey <--> User
    # userkey

    # @ManyToMany : User <--> UserGroup
    usergroup = relationship("UserGroup", secondary=userGroup_Has_User_Table, backref="user")

    # @ManyToMany :  User <--> HostGroup/Rights
    hostgroup = relationship("User_Has_HostGroup_With_Rights", backref="user")

    # @ManyToMany :  User <--> Host/Rights
    host = relationship("User_Has_Host_With_Rights", backref="user")

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

