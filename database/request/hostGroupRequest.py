#!/usr/bin/env python                                                                                          

import sqlalchemy
From sqlalchemy import *
from sqlalchemy.orm import *

# A class to perform transaction with 'hostgroup' table
class hostGroupRequest():

    # Get the hostgroup object associated to the given id
    def getHostGroupById(self, sid):
        session = Session()
        hostgroup = session.query(HostGroup).filter_by(id=sid).one()
        return hostgroup

    # Add the given HostGroup mapped object to the database
    def addHostGroup(self, hostgroup):
        session = Session()
        session.add(hostgroup)
        session.commit()

    # Delete the hostgroup column associated to the given ig
    def removeHostGroupById(self, sid):
        session = Session()
        hostgroup = session.query(HostGroup).filter_by(id=sid).one()
        session.delete(hostgroup)
        session.commit()

    # Delete the given HostGroup mapped object from the database
    def removeHostGroup(self, hostgroup):
        session = Session()
        session.delete(hostgroup)
        session.commit()
