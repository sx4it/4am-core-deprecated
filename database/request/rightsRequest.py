#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from database.entity import rights

# TODO review!!

# A class to perform transaction with 'rights' table
class RightsRequest():

    def __init__(self, sess):
        self._session = sess

    def getRights(self):
        ret = self._session.query(rights.Rights).all()
        return ret

    # Get the rights object associated to the given id
    def getRightsById(self, sid):
        ret = self._session.query(rights.Rights).filter_by(id=sid).one()
        return ret

    # Add the given mapped object to the database
    def addRights(seld, rights):
        self._session.add(rights)
        self._session.commit()

    # Delete the rights column associated to the given id
    def removeRightsById(self, sid):
        ret = self._session.query(rightsRights).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()

    # Delete the given mapped object from the database
    def removeRights(self, rights):
        self._session.delete(rights)
        self._session.commit()
