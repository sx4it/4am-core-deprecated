#!/usr/bin/env python

from sqlalchemy import Column, Integer, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref

from database.base import Base

# A ManyToMany association table between UserGroup and User
userGroup_Has_User_Table = Table('usergroup_has_user', Base.metadata,
                                 Column('user_id', Integer, ForeignKey('user.id')),
                                 Column('usergroup_id', Integer, ForeignKey('usergroup.id'))
                                 )


# A ManyToMany association table between HostGroup and Host
hostGroup_Has_Host_Table = Table('hostgroup_has_host', Base.metadata,
                                 Column('host_id', Integer, ForeignKey('host.id')),
                                 Column('hostgroup_id', Integer, ForeignKey('hostgroup.id'))
                                 )


# A ManyToMany association table between User, HostGroup and Rights
class User_Has_HostGroup_With_Rights(Base):
    __tablename__ = 'user_has_hostgroup_with_rights'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    hostgroup_id = Column(Integer, ForeignKey('hostgroup.id'), primary_key=True)
    rights_id = Column(Integer, ForeignKey('rights.id'), primary_key=True)
    hostgroup = relationship("HostGroup", backref="user_has_hostgroup_with_rights")
    rights = relationship("Rights", backref="user_has_hostgroup_with_rights")


# A ManyToMany association table between User, Host and Rights
class User_Has_Host_With_Rights(Base):
    __tablename__ = 'user_has_host_with_rights'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'), primary_key=True)
    rights_id = Column(Integer, ForeignKey('rights.id'), primary_key=True)
    host = relationship("Host", backref="user_has_host_with_rights")
    rights = relationship("Rights", backref="user_has_host_with_rights")


# A ManyToMany association table between UserGroup, Host and Rights
class UserGroup_Has_Host_With_Rights(Base):
    __tablename__ = 'usergroup_has_host_with_rights'
    usergroup_id = Column(Integer, ForeignKey('usergroup.id'), primary_key=True)
    host_id = Column(Integer, ForeignKey('host.id'), primary_key=True)
    rights_id = Column(Integer, ForeignKey('rights.id'), primary_key=True)
    host = relationship("Host", backref="usergroup_has_host_with_rights")
    rights = relationship("Rights", backref="usergroup_has_host_with_rights")


# A ManyToMany association table between UserGroup, HostGroup and Rights
class UserGroup_Has_HostGroup_With_Rights(Base):
    __tablename__ = 'usergroup_has_hostgroup_with_rights'
    usergroup_id = Column(Integer, ForeignKey('usergroup.id'), primary_key=True)
    hostgroup_id = Column(Integer, ForeignKey('hostgroup.id'), primary_key=True)
    rights_id = Column(Integer, ForeignKey('rights.id'), primary_key=True)
    hostgroup = relationship("HostGroup", backref="usergroup_has_hostgroup_with_rights")
    rights = relationship("Rights", backref="usergroup_has_hostgroup_with_rights")
