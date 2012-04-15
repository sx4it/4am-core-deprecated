'''
Server singleton in the form of a module.
'''

import zmq
import paramiko
import os
import logging

from common.jsonrpc import call

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
        ## The HostKeys should be loaded on the client side and streamed to the server
        self.remoteHostKeysFile = os.path.expanduser('~/.4am/known_hosts')
        #remoteHostKeys = paramiko.HostKeys(remoteHostKeysFile)
        self.remoteHostKeys = paramiko.HostKeys()

    def configure(self, socketURI):
        '''
        Takes the port and the databaseOpts as parameter.
        '''
        if self.__configured == True:
            raise RuntimeError("Attempted to reconfigure an already configured instance.")
        self.__socketURI = socketURI
        self.__socket.bind(self.__socketURI)
        self.__configured = True
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
        return hasattr(Server, "_instance")

    def run(self):
        """
        """
        import api
        self.__run = True
        while self.__run:
            ## FIXME: For debug purpose
            reload(api)
            res = call.processCall(self.__socket.recv(), api)
            logging.debug('processCall result : %s', res)
            self.__socket.send(res)

