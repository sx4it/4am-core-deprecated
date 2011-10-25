#!/usr/bin/env python

import zmq, sys

if __name__ == "__main__":
	try:
		port = sys.argv[1]
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://127.0.0.1:" + port)
		while True:
			b = socket.recv_json()
			#print port + "_recv >> ", b
			b['server'] = port
			b['status'] = 'ok'
			b['toto'] += 1
			socket.send_json(b)
	except KeyboardInterrupt:
		print "ending control" + port
