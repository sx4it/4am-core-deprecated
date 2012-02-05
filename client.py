#!/usr/bin/env python

import paramiko
import json
import socket
import logging
import unittest
import base64
from jsonrpc import proxy, call
import os, sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("", "--user-key", dest="user_key",
                  help="client private key path", metavar="USER_KEY_PATH", default="~/.ssh/id_rsa")
parser.add_option("-p", "--port", dest="port", type="int",
                  help="port of the client", metavar="PORT", default=2200)
parser.add_option("-a", "--addr", dest="ip",
                  help="ip of the client", metavar="IP_ADDRESS", default="127.0.0.1")

def loadkey(key):
	return paramiko.RSAKey(filename=key)

class Client:
	def __init__(self, **option):
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		po = paramiko.WarningPolicy()
		self.client.set_missing_host_key_policy(po)
		self.client.connect(option['host'], option['port'], option['user'], pkey=loadkey("/tmp/martial"))
		self.chan = self.client.get_transport().open_channel('sx4it_command')
	def __call__(self, args):
# put an id into jsonrpc requests
		params = []
		if len(args) == 0:
			raise RuntimeError("Please give at least function name !")
		elif len(args) > 1:
			params = args[1:]
		if args[0].find('.') == -1:
			args[0] = args[0] + "." + args[0]
		postdata = call.forgeJRPC(args[0], 'jsonrpc', params)
		self.chan.send(postdata + "\r")
		res = self.chan.recv(2048)
		logging.debug('recieving %s', res)
		return call.analyzeJRPCRes(res)

if __name__ == "__main__":
	(options, args) = parser.parse_args()
	#logging.basicConfig(level=logging.DEBUG)
	client = Client(host=options.ip, port=options.port, user=os.getenv('USER'))
	try:
		print client(args)
	except call.JRPCError as error:
		print "Fatal Error:"
		print error
