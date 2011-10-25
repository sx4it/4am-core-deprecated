#!/usr/bin/env python

import paramiko
import json
import os, socket, threading, base64, Queue, time

PORT = 2200

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
	def _validate(self, str):
		b = json.loads(str)
		b['result'] = True
		b['server'] = 'is cool'
		b['toto'] += 1
		self.to_send.append(json.dumps(b))

class SSHShellSession(SSHChanHandler):
	def _validate(self, str):
		self.to_send.append("Recv >" + str + "\r\n")

def Worker():
	run = True
	sessions = []
	while run:
		sleep = []
		map(lambda b : sleep.append(b()), sessions)
		if not True in sleep:
			time.sleep(0.1)
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
						sessions.append(SSHCommandSession(chan))
					elif server.chan_name == 'session':
						sessions.append(SSHShellSession(chan))
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

	def run(self):
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

if __name__ == "__main__":
	paramiko.util.log_to_file('demo_server.log')
	server = Server()
	server.run()
