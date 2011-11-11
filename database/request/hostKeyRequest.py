#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'hostkey' table
class hostKeyRequest():

    # Get the hostkey object associated to the given id
    def getHostKeyById(sid):
        session = Session()
        hostkey = session.query(HostKey).filter_by(id=sid).one()
        return hostkey

    # Add the given mapped object to the database
    def addHostKey(seld, hostkey):
        session = Session()
        session.add(hostkey)
        session.commit()

    # Delete the hostkey column associated to the given id
    def removeHostKeyById(sid):
        session = Session()
        hostkey = session.query(HostKey).filter_by(id=sid).one()
        session.delete(hsostkey)
        session.commit()

    # Delete the given mapped object from the database
    def removeHostKey(hostkey):
        session = Session()
        session.delete(hostkey)
        session.commit()
