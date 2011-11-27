#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq, multiprocessing
import os, socket, threading, base64, Queue, time
import select

PORT = 2200
PORTLIST = range(5000, 5010) # Add 10 Controlers

print PORTLIST

def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return paramiko.RSAKey(data=base64.decodestring(b))

b = loadkey('~/.ssh/id_rsa.pub')
USERS = { 'chatel_b': b, 'foo': b}

class SSHChanHandler(object):
	def __init__(self, chan):
		self.chan = chan
		self.chan.settimeout(None)
		self.to_send = []
		self.str = ""
		self.poll = zmq.core.poll.Poller() # using zmq poll to monitor all socks in reading
		self.poll.register(self.chan, flags=zmq.POLLIN)
	def fileno(self):
		return self.chan.fileno()
	def __call__(self):
		self._send()
		poll = dict(self.poll.poll(timeout=2))
		if self.chan.fileno() in poll.keys():
			self._recv()
		return poll
	def _recv(self):
		s = self.chan.recv(2048)
		if not len(s):
			raise IOError("session finish")
		self.str += s
		print "str" + self.str
		split = self.str.split("\r")
		if len(split) > 1:
			self._validate(split[0])
			self.str = ""
			self.str.join(split[1:])
	def _send(self):
		if self.chan.send_ready() and len(self.to_send) > 0:
			for b in self.to_send:
				print "Sending >", b
				self.chan.send(b)
			self.to_send = []
	def _validate(self):
		pass
	def shutdown(self):
		self.chan.close()

class SSHCommandSession(SSHChanHandler):
	def __init__(self, chan):
		super(SSHCommandSession, self).__init__(chan)
		context = zmq.Context()
		self.sock = context.socket(zmq.REQ)
		for port in PORTLIST:
			self.sock.connect("tcp://127.0.0.1:" + str(port))
		self.poll.register(self.sock, flags=zmq.POLLIN)
	def _validate(self, str):
		self.sock.send(str) # forward to server via zmq
	def __call__(self):
		poll = super(SSHCommandSession, self).__call__()
		if poll.has_key(self.sock):
			recv = self.sock.recv()
			self.to_send.append(recv)

class SSHShellSession(SSHChanHandler):
	def __init__(self, chan):
		super(SSHShellSession, self).__init__(chan)
		self.to_send = ["Hello ! Welcome to sx4it !\r\n", "$>"]
	def _validate(self, str):
		self.to_send.append("recv <" + str + ">\r\n" + "$>")
		#TODO prompt a shell for the user. and forward when ready json to server

def Worker(client, host_key):
	run = True
	t = paramiko.Transport(client)
	t.load_server_moduli()
	t.add_server_key(host_key)
	server = SSHHandler()
	t.start_server(server=server)
	chan = t.accept(1)
	if chan is not None:
		server.event.wait(10)
		if not server.event.isSet():
			print "no such session"
			sys.exit(1)
		else:
			file = chan.makefile()
			if server.chan_name == 'sx4it_command':
				session = SSHCommandSession(chan)
			elif server.chan_name == 'session':
				session = SSHShellSession(chan)
			else:
				print "no such session"
				sys.exit(1)
	else:
		print "Auth fail"
		sys.exit(1)
	while run:
		session()
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
	paramiko.util.log_to_file('demo_server.log')
	server = Server()
	server.run()
