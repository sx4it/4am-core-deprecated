#!/usr/bin/env python                                                                                          

import sqlalchemy
from sqlalchemy import *
from sqlalchemy.orm import *

from database.entity import hostGroup

# A class to perform transaction with 'hostgroup' table
class HostGroupRequest():

    def __init__(self, sess):
        self._session = sess

    # Get the hostgroup object associated to the given id
    def getHostGroupById(self, sid):
        ret = self._session.query(hostGroup.HostGroup).filter_by(id=sid).one()
        return ret

    # Add the given HostGroup mapped object to the database
    def addHostGroup(self, hostgroup):
        self._session.add(hostgroup)
        self._session.commit()

    # Delete the hostgroup column associated to the given ig
    def removeHostGroupById(self, sid):
        ret = self._session.query(hostGroup.HostGroup).filter_by(id=sid).one()
        self._session.delete(ret)
        self._session.commit()

    # Delete the given HostGroup mapped object from the database
    def removeHostGroup(self, hostgroup):
        self._session.delete(hostgroup)
        self._session.commit()
