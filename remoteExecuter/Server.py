
import zmq
import call
import api
import paramiko
import os
import logging

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5001")

## The HostKeys should be loaded on the client side and streamed to the server
remoteHostKeysFile = os.path.expanduser('~/.4am/known_hosts')
#remoteHostKeys = paramiko.HostKeys(remoteHostKeysFile)
remoteHostKeys = paramiko.HostKeys()

def run():
    while True:
        ## FIXME: For debug purpose
        reload(api)
        res = call.processCall(socket.recv(), api)
        logging.debug('processCall result : %s', res)
        socket.send(res)

