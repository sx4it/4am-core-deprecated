#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'userkey' table
class userKeyRequest():

    # Get the userKey object associated to the given id
    def getUserKeyById(sid):
        session = Session()
        userkey = session.query(UserKey).filter_by(id=sid).one()
        return userkey

    # Add the given mapped object to the database
    def addUserKey(seld, userkey):
        session = Session()
        session.add(userkey)
        session.commit()

    # Delete the userkey column associated to the given id
    def removeUserKeyById(sid):
        session = Session()
        userkey = session.query(UserKey).filter_by(id=sid).one()
        session.delete(userkey)
        session.commit()

    # Delete the given mapped object from the database
    def removeUserKey(userkey):
        session = Session()
        session.delete(userkey)
        session.commit()
