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

    # Get all user
    def getAllUser(self):
        ret = self._session.query(user.User).all()
        return ret

    # Get the user object associated to the given login
    def getUser(self, name):
        ret = self._session.query(user.User).filter_by(login=name).one()
        return ret

    # Add the given mapped object to the database
    def addUser(self, usr):
        self._session.add(usr)
        self._session.commit()

    # Delete the user column associated to the given login
    def deleteUser(self, username):
        usr = self._session.query(user.User).filter_by(login=username).one()
        self._session.query(userKey.UserKey).filter_by(user_id=usr.id).delete(synchronize_session=False)
        self._session.delete(usr)
        self._session.commit()


