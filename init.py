#!/usr/bin/env python

from database.entity import *
import os, sys

from common.sx4itconf.Sx4itConf import ArgsAndFileParser

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

#TODO CLEANN !!!
try:
  opts = ArgsAndFileParser()
  opts.addArgsParser(parser)
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
  print "Succeed."
else:
  print "Failed !!! (userkey already in db ?)"
