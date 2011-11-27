#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import base 

from entity import *
from request import *

class SqlAlchemySession:

    def __init__(self, host):

        print sqlalchemy.__version__

        # Create engine
        self._engine = create_engine(host, echo = False)

        # Auto create all table in db if not exist
        base.Base.metadata.create_all(self._engine, checkfirst = True)

        # SqlAlchemy session
        Session = sessionmaker(bind = self._engine)
        self._session = Session()

        self._userRequest = userRequest.UserRequest(self._session)
        self._userKeyRequest = userKeyRequest.UserKeyRequest(self._session)
        self._userGroupRequest = userGroupRequest.UserGroupRequest(self._session)
        self._rightsRequest = rightsRequest.RightsRequest(self._session)
        self._hostRequest = hostRequest.HostRequest(self._session)
        self._hostKeyRequest = hostKeyRequest.HostKeyRequest(self._session)
        self._hostGroupRequest = hostGroupRequest.HostGroupRequest(self._session)
