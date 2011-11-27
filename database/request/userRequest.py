#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import user

# A class to perform transaction with 'user' table
class UserRequest():

    def __init__(self, sess):
        self._session = sess
    
    # Get the user object associated to the given id
    def getUserById(self, sid):
        ret = self._session.query(user.User).filter_by(id=sid).one() 
        return ret

    # Add the given mapped object to the database
    def addUser(self, user):
        self._session.add(user)
        self._session.commit()

    # Delete the user column associated to the given id
    def removeUserById(self, sid):
        ret = self._session.query(user.User).filter_by(id=sid).one() 
        self._session.delete(ret)
        self._session.commit()

    # Delete the given mapped object from the database
    def removeUser(self, user):
        self._session.delete(user)
        self._session.commit()


