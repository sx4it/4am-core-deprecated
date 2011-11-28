#!/usr/bin/env python

import zmq
import json
import logging

class Proxy(object):
    """
    """
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

