#!/usr/bin/env python

import zmq
import jsonrpc
import demo_jrpcapi
import logging

logging.basicConfig(level=logging.DEBUG)
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5000")

while True:
    res = jsonrpc.processCall(socket.recv(), demo_jrpcapi)
    logging.debug('processCall result : %s', res)
    socket.send(res)

