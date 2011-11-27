#!/usr/bin/env python

import paramiko
import json
from jsonrpc import proxy

hostname = 'localhost'
port = 2200
username = 'foo'

class Client(proxy.Proxy):
	def __init__(self):
		super(Client, self).__init__('User')
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(paramiko.WarningPolicy)
		self.client.connect(hostname, port, username)
		self.chan = self.client.get_transport().open_channel('sx4it_command')
	def __call__(self, *args, **kwargs):
		postdata = super(Client, self).__call__(args, kwargs)
		self.chan.send(postdata + "\r")
		print self.chan.recv(2048)

if __name__ == "__main__":
	client = Client()
	for b in range(10):
		client.add('toto')
	client.delete('toto')
