#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq, multiprocessing
import os, socket, threading, base64, Queue, time
import select
import logging
import ConfigParser

from optparse import OptionParser

from sshhandler import shell, sx4itsession

import jsonrpc.proxy
import zmq

parser = OptionParser()
parser.epilog = "Theses option are overwritting the default configuration file ('server.conf'), if no configuration file is present, the server need theses values to be set."
parser.add_option("-c", "--controler", dest="controller_number",
		  help="number of controllers to launch", metavar="NB_CONTROLLER")
parser.add_option("-p", "--port", dest="server_port",
		  help="the port of the server", metavar="PORT_NB")
parser.add_option("", "--controller-port", dest="controller_port",
		  help="the starting port of the controllers", metavar="PORT_NB")
parser.add_option("", "--database-port", dest="database_port",
		  help="database port", metavar="PORT_NB")
parser.add_option("", "--database-ip", dest="database_ip",
		  help="database ip", metavar="IP")
parser.add_option("", "--database-user", dest="database_user",
		  help="database user", metavar="USER")
parser.add_option("", "--database-pass", dest="database_pass",
		  help="database pass", metavar="PASS")
parser.add_option("", "--database-name", dest="database_name",
		  help="database name", metavar="NAME")
parser.add_option("", "--database-controller", dest="database_controller",
		  help="database controller", metavar="controller")

class UsageException(BaseException):
	def __init__(self, key):
		self.key = key
	def __str__(self):
		return "No %s used, check your server.conf or your command line."%str(self.key)

class ArgsAndFileParser(object):
	def __init__(self):
		self.opts = {}
		(options, args) = parser.parse_args()
		opt = options.__dict__
		config = ConfigParser.RawConfigParser()
		config.read("server.conf")
		self.loadItemsFromSection(config, "server")
		self.loadItemsFromSection(config, "controller")
		self.loadItemsFromSection(config, "database")
		for b in opt:
			if opt[b] is not None:
				self.opts[b] = opt[b]
	def __str__(self):
		return str(self.opts)
	def __getitem__(self, key):
		if self.opts.get(key) is None:
			raise UsageException(key)
		return self.opts.get(key)
	def loadItemsFromSection(self, config, section):
		d = {}
		if not config.has_section(section):
			return
		for b in config.items(section):
			d[section + "_" + b[0]] = b[1]
		self.opts = dict(self.opts.items() + d.items())

#TODO CLEANN !!!
try:
	opts = ArgsAndFileParser()
	print opts
except UsageException as e:
	print "Error !", e
	parser.print_help()
	sys.exit(1)


class ControllerProxy(jsonrpc.proxy.Proxy):
	def __init__(self):

		portlist = range(int(opts["controller_port"]), int(opts["controller_port"]) + int(opts["controller_number"]))
		super(ControllerProxy, self).__init__()
		context = zmq.Context()
		self.sock = context.socket(zmq.REQ)
		for port in portlist:
			self.sock.connect("tcp://127.0.0.1:" + str(port)) #TODO use dynamic IP
	def __call__(self, *args, **kwargs):
		postdata = super(ControllerProxy, self).__call__(args, kwargs)
		self.sock.send(postdata)
		recv = self.sock.recv()
		return jsonrpc.proxy.analyzeJRPCRes(recv)

controllerProxy = ControllerProxy()

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
	chan = t.accept(20)
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
				print "making shell"
				session = shell.shell(chan, portlist)
			else:
				print "wtf shell"
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
		if controllerProxy.User.checkPassFromUsername(username, password): #TODO pb with password auth, it block
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	def check_auth_publickey(self, username, key):
		userkey = controllerProxy.User.getKeyFromUsername(username)
		if key == paramiko.RSAKey(data=base64.decodestring(userkey)):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	def get_allowed_auths(self, username):
		return 'password,publickey'
	def check_channel_shell_request(self, channel):
		self.event.set()
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
		self.proc.append(subprocess.Popen(['./control.py', str(port), json.dumps(opts.opts)], stdout=sys.stdout, stderr=sys.stdout))
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
	try:
		portlist = range(int(opts["controller_port"]), int(opts["controller_port"]) + int(opts["controller_number"]))
		logging.basicConfig(level=logging.DEBUG)
		logging.debug("server is listenning port -> %s", int(opts["server_port"]))
		logging.debug("launching controlers -> %s", portlist)
		paramiko.util.log_to_file('demo_server.log')
		server = Server(int(opts["server_port"]))
		server.run(portlist)
	except UsageException as e:
		print "Error !", e
		parser.print_help()
