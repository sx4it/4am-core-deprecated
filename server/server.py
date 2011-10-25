#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq
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

queue = Queue.Queue()

#TODO check if the socket shut

class SSHChanHandler(object):
	def __init__(self, chan):
		self.chan = chan
		self.to_send = []
		self.str = ""
	def __call__(self):
		recv = self._recv()
		send = self._send()
		return (recv or send)
	def _recv(self):
		event = False
		if self.chan.recv_ready():
			event = True
			s = self.chan.recv(2048)
			self.str += s
			split = self.str.split("\r")
			if len(split) > 1:
				self._validate(split[0])
				self.str = ""
				self.str.join(split[1:])
		return event
	def _send(self):
		event = False
		for b in self.to_send:
			if self.chan.send_ready():
				event = True
				print "Sending >", b
				self.chan.send(b)
				self.to_send.remove(b)
		return event
	def _validate(self):
		pass
	def shutdown(self):
		self.chan.shutdown(2)

class SSHCommandSession(SSHChanHandler):
	def __init__(self, chan):
		super(SSHCommandSession, self).__init__(chan)
		context = zmq.Context()
		self.sock = context.socket(zmq.REQ)
		for port in PORTLIST:
			self.sock.connect("tcp://127.0.0.1:" + str(port))
		self.poll = zmq.core.poll.Poller()
		self.poll.register(self.sock, flags=zmq.POLLIN)
	def _validate(self, str):
		self.sock.send(str) # forward to server via zmq
	def __call__(self):
		event = False
		b = super(SSHCommandSession, self).__call__()
		poll = self.poll.poll(timeout=0)
		if len(poll) > 0:
			recv = self.sock.recv()
			self.to_send.append(recv)
			event = True
		return b or event

class SSHShellSession(SSHChanHandler):
	def _validate(self, str):
		self.to_send.append("Recv >" + str + "\r\n")
		#TODO prompt a shell for the user. and forward when ready json to server

def Worker():
	run = True
	sessions = []
	while run:
		sleep = []
		map(lambda b : sleep.append(b()), sessions)
		if not queue.empty():
			try:
				client, host_key = queue.get()
			except:
				run = False
				break
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
				else:
					if server.chan_name == 'sx4it_command':
						sessions.append(SSHCommandSession(chan))#.makefile()))
					elif server.chan_name == 'session':
						sessions.append(SSHShellSession(chan))#.makefile()))
					else:
						print "no such session"
			else:
				print "Auth fail"
			queue.task_done()
	map(lambda b: b.shutdown, sessions)
	queue.task_done()

class SSHHandler(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()
		self.chan_name = ""
	def check_channel_request(self, kind, chanid):
		self.chan_name = kind
		if kind == 'session':
			self.event.set()
			return paramiko.OPEN_SUCCEEDED
		elif kind == 'sx4it_command':
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
		thread = threading.Thread(target=Worker)
		thread.deamon = True
		thread.start()
		try:
			while True:
				client, addr = self.sock.accept()
				queue.put((client, host_key))
		except KeyboardInterrupt:
			queue.put(None)
			queue.join()
			thread.join()
			map(lambda b : b.kill(), self.proc)


if __name__ == "__main__":
	paramiko.util.log_to_file('demo_server.log')
	server = Server()
	server.run()
