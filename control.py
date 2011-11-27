#!/usr/bin/env python

import zmq, sys
from jsonrpc import call
import api

if __name__ == "__main__":
	try:
		port = sys.argv[1]
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://127.0.0.1:" + port)
		while True:
			b = socket.recv()
			res = call.processCall(b, api)
			print port + "___recv___ >> ", b
			print port + "___job___ >> ", res
			socket.send_json(res)
	except KeyboardInterrupt:
		print "ending control" + port
