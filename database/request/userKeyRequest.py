#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import userKey

# A class to perform transaction with 'userkey' table
class UserKeyRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the userKey object associated to the given id
    def getUserKeyById(sid):
        ret = self._session.query(userKey.UserKey).filter_by(id=sid).one()
        return ret

    # Add the given mapped object to the database
    def addUserKey(seld, userkey):
        self._session.add(userkey)
        self._session.commit()

    # Delete the userkey column associated to the given id
    def removeUserKeyById(sid):
        ret = self._session.query(UserKey).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()

    # Delete the given mapped object from the database
    def removeUserKey(userkey):
        self._session.delete(userkey)
        self._session.commit()
