#!/usr/bin/env python2.7

import zmq
import inspect
import logging
import sqlalchemy.exc

from common import *
from common.jsonrpc import call
import ast
import api
import database
from remoteexecd.proc import Proxy as rEProxy

class DatabaseError(Exception):
    pass

class Server:
    def __init__(self):
        '''
        Init a server object.
        It only creates a zmq Context and socket.
        The created server still needs to be configured with the configure method.
        '''
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REP)
        self.__configured = False

    def configure(self, addr, remoteaddr, database_url):
        '''
        Takes the port and the databaseOpts as parameter.

        :database_url:
            database address in the form
            engine://user:pass@host:port/database
        '''
        if self.__configured == True:
            raise RuntimeError("Attempted to reconfigure an already configured instance.")
        self.__addr = addr
        self.__socket.bind(addr)
        try:
            self.db = database.Session(database_url)
        except sqlalchemy.exc.OperationalError as e:
            raise DatabaseError('Error during the database initialization \
"{0}".'.format(e))
        self.__configured = True
        self.rE = rEProxy(remoteaddr)
        return True

    @staticmethod
    def instance():
        """
        Returns a global Server instance.
        """
        if not hasattr(Server, "_instance"):
            Server._instance = Server()
        return Server._instance

    @staticmethod
    def initialized():
        """
        Returns true if the singleton instance has been created.
        """
        return hasattr(Server, "_instance")

    def run(self):
        """
        Entry point for the Controller function.
        The controller is biding a zmq socket on the port given, it wait for a JsonRPC call.
          .. note::
            for the moment we are reloading the api at each call, this is very bad for perfomance (it increase each call time by 200%)
            but it realy improve the developpement speed on the api component.
        """
        if self.__configured != True:
            raise RuntimeError("Can not start an unconfigured Server instance.")
        logging.debug("Launching server controller on port " + self.__addr)
        self.__run = True
        while self.__run:
            b = self.__socket.recv()
            # reload each time for testing :)
            reload(api)
            for name in dir(api):
                member = getattr(api, name)
                if inspect.ismodule(member):
                    reload(member)
            logging.debug(self.__addr + "___recv___ >> %s", b)
            res = call.processCall(b, api)
            logging.debug(self.__addr + "___job___ >> %s", res)
            self.__socket.send(res)

