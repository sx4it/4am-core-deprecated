#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'user' table
class userRequest():
    
    # Get the user object associated to the given id
    def getUserById(self, sid):
        session = Session()
        user = session.query(User).filter_by(id=sid).one() 
        return user

    # Add the given mapped object to the database
    def addUser(self, user):
        session = Session()
        session.add(user)
        session.commit()

    # Delete the user column associated to the given id
    def removeUserById(self, sid):
        session = Session()
        user = session.query(User).filter_by(id=sid).one() 
        session.delete(user)
        session.commit()

    # Delete the given mapped object from the database
    def removeUser(self, user):
        session = Session()
        session.delete(user)
        session.commit()


