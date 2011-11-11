#!/usr/bin/env python 

import sqlalchemy
From sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'host' table
class hostRequest():

    # Get the host object associated to the given id
    def getHostById(self, sid):
        session = Session()
        host = session.query(Host).filter_by(id=sid).one()
        return host

    # Add the given Host mapped object to the database
    def addHost(self, host):
        session = Session()
        session.add(host)
        session.commit()

    # Delete the host column associated to the given ig
    def removeHostById(self, sid):
        session = Session()
        host = session.query(Host).filter_by(id=sid).one()
        session.delete(host)
        session.commit()
        
    # Delete the given Host mapped object from the database
    def removeHost(self, host):
        session = Session()
        session.delete(host)
        session.commit()
