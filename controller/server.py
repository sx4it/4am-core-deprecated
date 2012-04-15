#!/usr/bin/env python2.7

import zmq
import inspect
import logging

from common import *
from common.jsonrpc import call
import ast
import api
import database

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

    def configure(self, port, databaseOpts):
        '''
        Takes the port and the databaseOpts as parameter.
        '''
        if self.__configured == True:
            raise RuntimeError("Attempted to reconfigure an already configured instance.")
        self.__port = port
        self.__configured = True
        self.__dbOpts = databaseOpts
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
        """Returns true if the singleton instance has been created."""
        return hasattr(IOLoop, "_instance")

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
        logging.debug("Launching server controller on port " + self.__port)
        self.__socket.bind("tcp://127.0.0.1:" + self.__port)
        self.db = database.InitSession(self.__dbOpts)
        self.__run = True
        logging.debug("Succesfully launched server controller on port " + self.__port)
        while self.__run:
            b = self.__socket.recv()
            # reload each time for testing :)
            reload(api)
            for name in dir(api):
                member = getattr(api, name)
                if inspect.ismodule(member):
                    reload(member)
            logging.debug(self.__port + "___recv___ >> %s", b)
            res = call.processCall(b, api)
            logging.debug(self.__port + "___job___ >> %s", res)
            self.__socket.send(res)

