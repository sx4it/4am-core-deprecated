#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from entity import hostKey

# A class to perform transaction with 'hostkey' table
class HostKeyRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the hostkey object associated to the given id
    def getHostKeyById(sid):
        ret = self._session.query(hostKey.HostKey).filter_by(id=sid).one()
        return ret

    # Add the given mapped object to the database
    def addHostKey(seld, hostkey):
        self._session.add(hostkey)
        self._session.commit()

    # Delete the hostkey column associated to the given id
    def removeHostKeyById(sid):
        ret = session.query(hostKey.HostKey).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()

    # Delete the given mapped object from the database
    def removeHostKey(hostkey):
        self._session.delete(hostkey)
        self._session.commit()
