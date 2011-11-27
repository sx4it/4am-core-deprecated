#!/usr/bin/env python

import zmq
import jsonrpc
import logging

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
        # The second param is the requestID.
        # It should be a usefull information to track the request if the call is asynchrone.
        postdata = jsonrpc.forgeJRPC(self.__callMeth, 'jsonrpc', args or kwargs)
        logging.debug('forged JRPC is : %s', postdata)
        self.__socket.send(postdata)
        return jsonrpc.analyzeJRPCRes(self.__socket.recv())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    context = zmq.Context()
    proxy = zmqREQServiceProxy(context, 'tcp://127.0.0.1:5000')
    print proxy.echo('toto')
 
