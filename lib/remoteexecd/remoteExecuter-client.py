#!/usr/bin/env python2.7

import logging
import os
import zmq
from common.jsonrpc import call

class zmqREQServiceProxy(object):
    """
    Basic JSONRPC Proxy using zmq.
    """
    def __init__(self, zmqContext, serviceURL, serviceName=None):
        self.__serviceURL = serviceURL
        self.__context = zmqContext
        self.__socket = zmqContext.socket(zmq.REQ)
        self.__socket.connect(serviceURL)
        self.__serviceName = serviceName

    def __getattr__(self, name):
        if self.__serviceName != None:
            name = "%s.%s" % (self.__serviceName, name)
        self.__callMeth = name
        return self

    def __call__(self, *args, **kwargs):
        if args and kwargs:
             raise RuntimeError('You cannot use both non-keyword arguments and keyword arguments at the same time.')
        postdata = call.forgeJRPC(self.__callMeth, 'jsonrpc', args or kwargs)
        logging.debug('forged JRPC is : %s', postdata)
        self.__socket.send(postdata)
        return call.analyzeJRPCRes(self.__socket.recv())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    context = zmq.Context()
    proxy = zmqREQServiceProxy(context, 'tcp://127.0.0.1:10000')
    # Stream the remoteHostKeys
    remoteHostKeysFile = os.path.expanduser('~/.4am/known_hosts')
    with open(remoteHostKeysFile) as f:
        for line in f:
            line = line.strip()
            if (len(line) == 0) or (line[0] == '#'):
                continue
            fields = line.split(' ') 
            if len(fields) < 3: 
                raise RuntimeError('Invalid fiel number')
            fields = fields[:3]
            names, keytype, key = fields 
            names = names.split(',') 
            proxy.addRemoteHostKey(names[0], keytype, key)
            proxy.dumpRemoteHostKey()
    HOST = '192.168.0.112'
    key = proxy.getRemoteHostKey(HOST, 22, 'ssh-rsa')
    proxy.addRemoteHostKey(HOST, 'ssh-rsa', key)
    proxy.dumpRemoteHostKey()
    proxy.delRemoteHostKey(HOST)
    proxy.dumpRemoteHostKey()
    #print proxy.addUserParamiko('toto', 'root', '/root/ct2', '192.168.0.112', 22)
    #print proxy.delUser('exploit', 'root', '/root/ct2', '192.168.0.112', 22)
 
