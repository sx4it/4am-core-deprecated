#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

# TODO review!!

# A class to perform transaction with 'rights' table
class rightsRequest():

    # Get the rights object associated to the given id
    def getRightsById(sid):
        session = Session()
        rights = session.query(Rights).filter_by(id=sid).one()
        return rights

    # Add the given mapped object to the database
    def addRights(seld, rights):
        session = Session()
        session.add(rights)
        session.commit()

    # Delete the rights column associated to the given id
    def removeRightsById(sid):
        session = Session()
        rights = session.query(Rights).filter_by(id=sid).one()
        session.delete(rights)
        session.commit()

    # Delete the given mapped object from the database
    def removeRights(rights):
        session = Session()
        session.delete(rights)
        session.commit()
