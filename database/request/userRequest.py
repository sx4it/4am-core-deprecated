#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from database.entity import user
from database.entity import userKey

# A class to perform transaction with 'user' table
class UserRequest():

    def __init__(self, sess):
        self._session = sess
    
    # Get the user object associated to the given id
    def getAllUser(self):
        ret = self._session.query(user.User).all()
        return ret

    # Get the user object associated to the given id
    def getUserById(self, sid):
        ret = self._session.query(user.User).filter_by(id=sid).one() 
        return ret

    # Get the user object associated to the given name
    def getUserByName(self, name):
        ret = self._session.query(user.User).filter_by(firstname=name).one() 
        return ret

    # Add the given mapped object to the database
    def addUser(self, user_):
        if self._session.query(user.User).filter_by(firstname=user_.firstname).count() != 0:
    return False
#TODO change to login ?
  self._session.add(user_)
  self._session.commit()
  return True

    # Delete the user column associated to the given id
    def removeUserById(self, sid):
        ret = self._session.query(user.User).filter_by(id=sid).one() 
  return removeUser(ret)

    # Delete the given mapped object from the database
    def removeUser(self, user):
        self._session.query(userKey.UserKey).filter_by(user_id=user.id).delete(synchronize_session=False)
        self._session.delete(user)
        self._session.commit()
        return True

