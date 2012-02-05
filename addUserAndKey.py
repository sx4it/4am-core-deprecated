#!/usr/bin/env python

from database.entity import *
import os

import ConfigParser

import database
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--key-path", dest="key_path",
		  help="key path", metavar="PATH", default="~/.ssh/id_rsa.pub")
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
	db_session = database.InitSession(opts)
except UsageException as e:
	print "Error !", e
	parser.print_help()
	sys.exit(1)

firstname = os.getenv('USER')
lastname = firstname
mail = firstname + '@sx4it.com'
password = firstname

def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return b

key = loadkey(opts["key_path"])

user1 = user.User(firstname, lastname, mail, password)
user1.userkey = [userKey.UserKey(key, 'type')]

if db_session._userRequest.addUser(user1) == True:
	print "Suceed."
