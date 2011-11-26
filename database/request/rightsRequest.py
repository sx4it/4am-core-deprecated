#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import rights

# TODO review!!

# A class to perform transaction with 'rights' table
class RightsRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the rights object associated to the given id
    def getRightsById(sid):
        ret = self.session.query(rights.Rights).filter_by(id=sid).one()
        return ret

    # Add the given mapped object to the database
    def addRights(seld, rights):
        self.session.add(rights)
        self.session.commit()

    # Delete the rights column associated to the given id
    def removeRightsById(sid):
        ret = self.session.query(rightsRights).filter_by(id=sid).one()
        self.session.delete(ret)
        self.session.commit()

    # Delete the given mapped object from the database
    def removeRights(rights):
        self.session.delete(rights)
        self.session.commit()
