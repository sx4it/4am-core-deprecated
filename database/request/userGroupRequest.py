#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'usergroup' table
class userGroupRequest():

    # Get the usergroup object associated to the given id
    def getUserGroupById(sid):
        session = Session()
        usergroup = session.query(UserGroup).filter_by(id=sid).one()
        return usergroup

    # Add the given mapped object to the database
    def addUserGroup(seld, usergroup):
        session = Session()
        session.add(usergroup)
        session.commit()

    # Delete the usergroup column associated to the given id
    def removeUserGroupById(sid):
        session = Session()
        usergroup = session.query(UserGroup).filter_by(id=sid).one()
        session.delete(usergroup)
        session.commit()

    # Delete the given mapped object from the database
    def removeUserGroup(usergroup):
        session = Session()
        session.delete(usergroup)
        session.commit()
