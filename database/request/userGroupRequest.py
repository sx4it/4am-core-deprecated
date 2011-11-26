#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import userGroup

# A class to perform transaction with 'usergroup' table
class UserGroupRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the usergroup object associated to the given id
    def getUserGroupById(sid):
        ret = self._session.query(userGroup.UserGroup).filter_by(id=sid).one()
        return ret

    # Add the given mapped object to the database
    def addUserGroup(seld, usergroup):
        self._session.add(usergroup)
        self._session.commit()

    # Delete the usergroup column associated to the given id
    def removeUserGroupById(sid):
        ret = session.query(UserGroup).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()

    # Delete the given mapped object from the database
    def removeUserGroup(usergroup):
        self._session.delete(usergroup)
        self._session.commit()
