#!/usr/bin/env python 

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import host

# A class to perform transaction with 'host' table
class HostRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the host object associated to the given id
    def getHostById(self, sid):
        ret = self._session.query(host.Host).filter_by(id=sid).one()
        return ret

    # Add the given Host mapped object to the database
    def addHost(self, host):
        self._session.add(host)
        self._session.commit()

    # Delete the host column associated to the given ig
    def removeHostById(self, sid):
        ret = self._session.query(host.Host).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()
        
    # Delete the given Host mapped object from the database
    def removeHost(self, host):
        self._session.delete(host)
        self._session.commit()
