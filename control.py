#!/usr/bin/env python

import zmq, sys
from jsonrpc import call
import logging
import ast
import api
import inspect

if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	try:
		port = sys.argv[1]
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://127.0.0.1:" + port)
		while True:
			b = socket.recv()
			# reload each time for testing :)
			reload(api)
			for name in dir(api):
				member = getattr(api, name)
				if inspect.ismodule(member):
					reload(member)
			res = call.processCall(b, api)
			logging.debug(port + "___recv___ >> %s", b)
			logging.debug(port + "___job___ >> %s", res)
			socket.send(res)
	except KeyboardInterrupt:
		logging.debug("ending control" + port)
