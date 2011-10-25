#!/usr/bin/env python

import paramiko
import json

hostname = 'localhost'
port = 2200
username = 'foo'

class Client(object):
	def __init__(self):
		self.client = paramiko.SSHClient()
		self.client.load_system_host_keys()
		self.client.set_missing_host_key_policy(paramiko.WarningPolicy)
		pass
	def connect(self):
		self.client.connect(hostname, port, username)
		c = self.client.get_transport().open_channel('sx4it_command')
		b = {}
		b["toto"] = 1
		b["method"] = 'hello'
		try:
			while True:
				c.send(json.dumps(b) + '\r')
				b = json.loads(c.recv(2048))
				if not b["toto"] < 4242:
					b["toto"] = 1
		except ValueError:
			print "server stoped :("

if __name__ == "__main__":
	client = Client()
	client.connect()
