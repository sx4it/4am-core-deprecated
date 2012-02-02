#!/usr/bin/env python

import paramiko
import json
import socket
import logging
from jsonrpc import proxy
import os

from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", type="int",
                  help="port of the client", metavar="PORT", default=2200)
parser.add_option("-a", "--addr", dest="ip",
                  help="ip of the client", metavar="IP_ADDRESS", default="127.0.0.1")

class Client(proxy.Proxy):
	def __init__(self, **k):
		super(Client, self).__init__()
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		po = paramiko.WarningPolicy()
		self.client.set_missing_host_key_policy(po)
		self.client.connect(k['host'], k['port'], k['user'])
		self.chan = self.client.get_transport().open_channel('sx4it_command')
	def __call__(self, *args, **kwargs):
		postdata = super(Client, self).__call__(args, kwargs)
		self.chan.send(postdata + "\r")
		logging.debug('recieving %s', self.chan.recv(2048))

if __name__ == "__main__":
	(options, args) = parser.parse_args()
	logging.basicConfig(level=logging.DEBUG)
#	try:
	client = Client(host=options.ip, port=options.port, user=os.getenv('USER'))
	for b in range(10):
		client.User.add(name='toto', passwd='123456')
		client.User.delete(name='toto')
		client.User.deletee('t', 'w')

#except socket.error:
	logging.error("Error connecting to server.")
