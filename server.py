#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq, multiprocessing
import os, socket, threading, base64, Queue, time
import select
import logging

from sshhandler import shell, sx4itsession

PORT = 2200
PORTLIST = range(5000, 5010) # Add 10 Controlers

def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return paramiko.RSAKey(data=base64.decodestring(b))

b = loadkey('~/.ssh/id_rsa.pub')
USERS = { 'chatel_b': b, 'foo': b}

def Worker(client, host_key):
	t = paramiko.Transport(client)
	t.load_server_moduli()
	t.add_server_key(host_key)
	server = SSHHandler()
	t.start_server(server=server)
	chan = t.accept(1)
	if chan is not None:
		server.event.wait(10)
		if not server.event.isSet():
			logging.error("no such session")
			sys.exit(1)
		else:
			file = chan.makefile()
			if server.chan_name == 'sx4it_command':
				session = sx4itsession.sx4itsession(chan, PORTLIST)
			elif server.chan_name == 'session':
				session = shell.shell(chan, PORTLIST)
			else:
				logging.error("no such session")
				sys.exit(1)
	else:
		logging.error("Auth fail.")
		sys.exit(1)
	try:
		while True:
			session()
	except:
		logging.info('connection closed.')
	session.shutdown()

class SSHHandler(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()
		self.chan_name = ""
	def check_channel_request(self, kind, chanid):
		self.chan_name = kind
		if kind == 'session' or kind == 'sx4it_command':
			self.event.set()
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	def check_auth_password(self, username, password):
		return paramiko.AUTH_FAILED
	def check_auth_publickey(self, username, key):
		if username in USERS.keys() and USERS[username] == key:
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	def get_allowed_auths(self, username):
		return 'publickey'
	def check_channel_shell_request(self, channel):
		return True
	def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
		pixelheight, modes):
		return True

class Server(object):
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', PORT))
		self.sock.listen(100)
		self.proc = []
	def LaunchController(self, port):
		self.proc.append(subprocess.Popen(['./control.py', str(port)], stdout=sys.stdout, stderr=sys.stdout))
	def run(self):
		for port in PORTLIST:
			self.LaunchController(port)
		host_key = paramiko.RSAKey(filename='test_rsa.key')
		thread = []
		try:
			while True:
				client, addr = self.sock.accept()
				thread.append(threading.Thread(target=Worker, args=(client, host_key)))
# thread.append(multiprocessing.Process(target=Worker, args=(client, host_key)))
# can't test with real thread... http://github.com/robey/paramiko/issues/27
				thread[-1].deamon = True
				thread[-1].start()
		except KeyboardInterrupt:
			map(lambda b : b.join(), thread)
			map(lambda b : b.kill(), self.proc)


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG)
	logging.debug("launching controlers -> %s", PORTLIST)
	paramiko.util.log_to_file('demo_server.log')
	server = Server()
	server.run()
