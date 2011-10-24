#!/usr/bin/env python

import paramiko
import os, socket, threading, base64, Queue

PORT = 2200

def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return paramiko.RSAKey(data=base64.decodestring(b))

b = loadkey('~/.ssh/id_rsa.pub')
USERS = { 'chatel_b': b, 'foo': b}

queue = Queue.Queue()

def Recv(to_recv, to_send):
	for b in to_recv:
		if b.recv_ready():
			s = b.recv(2048)
			print "Recv >" + s
			to_send[b] = "Recv >" + s

def Send(to_send):
	for b in to_send.keys():
		if b.send_ready():
			print "Sending >", to_send[b]
			b.send(to_send[b])
			del to_send[b]

def Worker():
	to_send = {}
	to_recv = []
	run = True
	while run:
		Recv(to_recv, to_send)
		Send(to_send)
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
				to_send[chan] = "Hello You :)\n"
				to_recv.insert(0, chan)
				server.event.wait(10)
				if not server.event.isSet():
					 raise '*** Client never asked for a shell.'
			else:
				print "Auth fail"
			queue.task_done()
	for s in to_recv:
		s.shutdown(2)
	queue.task_done()

class SSHHandler(paramiko.ServerInterface):
	def __init__(self):
		self.event = threading.Event()
	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
	def check_auth_password(self, username, password):
		#no password auth
		return paramiko.AUTH_FAILED
	def check_auth_publickey(self, username, key):
		if username in USERS.keys() and USERS[username] == key:
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	def get_allowed_auths(self, username):
		return 'publickey'
		#no password auth
		#return 'password,publickey'
	def check_channel_shell_request(self, channel):
		self.event.set()
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
