#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq, multiprocessing
import os, socket, threading, base64, Queue, time
import select
import logging

from database import Session
from database.entity import user
from optparse import OptionParser

from sshhandler import shell, sx4itsession



parser = OptionParser()
parser.add_option("-c", "--controler", dest="NB_CONTROLLER", type="int",
		  help="number of controllers to launch", metavar="NB_CONTROLLER", default=1)
parser.add_option("-p", "--port", dest="PORT", type="int",
		  help="the port of the server", metavar="PORT_NB", default=2200)
parser.add_option("-y", "--controller-port", dest="controller_port", type="int",
		  help="the starting port of the controllers", metavar="PORT_NB", default=5000)


def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return paramiko.RSAKey(data=base64.decodestring(b))

b = loadkey('~/.ssh/id_rsa.pub')
USERS = { 'chatel_b': b, 'foo': b}

def Worker(client, host_key, portlist):
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
				session = sx4itsession.sx4itsession(chan, portlist)
			elif server.chan_name == 'session':
				session = shell.shell(chan, portlist)
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
		user = Session._userRequest.getUserByName(username)
		if username == user.firstname and password == user.password:
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	def check_auth_publickey(self, username, key):
		user = Session._userRequest.getUserByName(username)
		if username == user.firstname and key in (paramiko.RSAKey(data=base64.decodestring(u.ukkey)) for u in user.userkey):
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
	def __init__(self, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind(('', port))
		self.sock.listen(100)
		self.proc = []
	def LaunchController(self, port):
		self.proc.append(subprocess.Popen(['./control.py', str(port)], stdout=sys.stdout, stderr=sys.stdout))
	def run(self, portlist):
		for port in portlist:
			self.LaunchController(port)
		host_key = paramiko.RSAKey(filename='test_rsa.key')
		thread = []
		try:
			while True:
				client, addr = self.sock.accept()
				thread.append(threading.Thread(target=Worker, args=(client, host_key, portlist)))
# thread.append(multiprocessing.Process(target=Worker, args=(client, host_key)))
# can't test with real thread... http://github.com/robey/paramiko/issues/27
				thread[-1].deamon = True
				thread[-1].start()
		except KeyboardInterrupt:
			map(lambda b : b.join(), thread)
			map(lambda b : b.kill(), self.proc)

if __name__ == "__main__":
	(options, args) = parser.parse_args()
	portlist = range(options.controller_port, options.controller_port + options.NB_CONTROLLER)
	logging.basicConfig(level=logging.DEBUG)
	logging.debug("server is listenning port -> %s", options.PORT)
	logging.debug("launching controlers -> %s", portlist)
	paramiko.util.log_to_file('demo_server.log')
	server = Server(options.PORT)
	server.run(portlist)
