#!/usr/bin/env python

import zmq
import json
import logging

class JRPCError(RuntimeError):
    def __init__(self, text):
        RuntimeError.__init__(self, text)

def forgeJRPC(method, requestId, *args, **kwargs):
	return json.dumps(dict(jsonrpc = '2.0', method = method, params = (args or kwargs), id = requestId))

def analyzeJRPCRes(rawres):
	resp = json.loads(rawres)
	if resp.get('error') != None:
        	raise JRPCError(resp['error'])
	return resp['result']

class Proxy(object):
	def __init__(self):
		self.__callMeth = ""
	def __getattr__(self, name):
		c = ''
		if self.__callMeth != "":
			c = '.'
		self.__callMeth += c + name
		return self
	def __call__(self, *args, **kwargs):
		postdata = forgeJRPC(self.__callMeth, 'jsonrpc', args or kwargs)
		self.__callMeth = ""
		logging.debug('forged JRPC is : %s', postdata)
		return postdata

class zmqREQServiceProxy(object):
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
	postdata = forgeJRPC(self.__callMeth, 'jsonrpc', args or kwargs)
	logging.debug('forged JRPC is : %s', postdata)
	self.__socket.send(postdata)
	return analyzeJRPCRes(self.__socket.recv())

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	context = zmq.Context()
	proxy = zmqREQServiceProxy(context, 'tcp://127.0.0.1:5000')
	print proxy.addKey('test')
