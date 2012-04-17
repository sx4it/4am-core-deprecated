#!/usr/bin/env python

import paramiko
import json, subprocess, sys, zmq, multiprocessing
import os, socket, threading, base64, Queue, time
import select
import logging
import ConfigParser

from optparse import OptionParser

from sshhandler import shell, sx4itsession

from common import *
from common.jsonrpc.zmqProxy import zmqREQServiceProxy
import zmq

from optparse import OptionParser

opts = {}

parser = OptionParser()
parser.epilog = "Theses option are overwritting the default configuration file ('server.conf'), if no configuration file is present, the server need theses values to be set."
parser.add_option("-c", "--controler", dest="controller_number",
      help="number of controllers to launch", metavar="NB_CONTROLLER")
parser.add_option("-d", "--debug", action="store_true", dest="debug",
      help="Debug mode", metavar="DEBUG", default=False)
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

try:
  from common.sx4itconf import Sx4itConf
  opts = Sx4itConf.opts
  opts.addArgsParser(parser)
  print opts
except Exception as e:
  print "Error !", e
  parser.print_help()
  sys.exit(1)

portlist = range(int(opts["controller_port"]), int(opts["controller_port"]) + int(opts["controller_number"]))
controllerProxy = zmqREQServiceProxy([ 'tcp://127.0.0.1:' + str(port) for port in portlist ])
del portlist

def loadkey(key):
  """
  This function load the server key and convert it to the desired paramiko format.
  """
  b = open(os.path.expanduser(key)).read().split()[1]
  return paramiko.RSAKey(data=base64.decodestring(b))

b = loadkey('~/.ssh/id_rsa.pub')
USERS = { 'chatel_b': b, 'foo': b}

def Worker(client, host_key, portlist):
  """
  The worker function is the entry point when a client is connecting to the server,
  it initialize paramiko context and check the connection channel.
  This function also launch the session handler and keep client informations.

  :host_key:
    this is the server key
  :portlist:
    this is the port list

  """
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
  except socket.error:
    logging.info('connection closed.')
  except IOError as e:
    logging.info('connection closed:' + str(e))
  session.shutdown()

class SSHHandler(paramiko.ServerInterface):
  """
  We inherit from the paramiko serverinterface and redefine our security behaviors.
    .. note:: we connect to via zmq to check the userkey
  """
  def __init__(self):
    self.event = threading.Event()
    self.chan_name = ""
  def check_channel_request(self, kind, chanid):
    """
    This function check the two different type of ssh sessions: **session** (the defautl ssh session) and **sx4it_command**.
    We only accept this two type of connection.
    """
    self.chan_name = kind
    if kind == 'session' or kind == 'sx4it_command':
      self.event.set()
      return paramiko.OPEN_SUCCEEDED
    return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
  def check_auth_password(self, username, password):
    """
    This is the function which check the password
    """
    if controllerProxy.User.checkPassFromUsername(user=username, password=password): #TODO pb with password auth, it block
      return paramiko.AUTH_SUCCESSFUL
    return paramiko.AUTH_FAILED
  def check_auth_publickey(self, username, key):
    """
    This function remotly check that the publickey is matching with the username.
    """
    userkey = controllerProxy.User.getKeyFromUsername(user = username)
    if len(userkey) and key == paramiko.RSAKey(data=base64.decodestring(userkey)):
      return paramiko.AUTH_SUCCESSFUL
    return paramiko.AUTH_FAILED
  def get_allowed_auths(self, username):
    """
    This function is getting the two type of allowed loggin mode.
    """
    return 'password,publickey'
  def check_channel_shell_request(self, channel):
    """
    This function is used to flag the connection type (for default ssh shell).
    """
    self.event.set()
    return True
  def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
    pixelheight, modes):
    """
    This function is to allow the pty allocation.
    """
    return True

class Server(object):
  """
  The server object hold the connection, it is the main loop for the server.
  """
  def __init__(self, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.sock.bind(('', port))
    self.sock.listen(100)
    self.proc = []

  def LaunchController(self, port):
    """
    This allow us to launch the child controller process.

    :port:
      this is the port where the controller will be listenning to

    """
    self.proc.append(subprocess.Popen(['./4am-controllerd', str(port), json.dumps(opts.opts)], stdout=sys.stdout, stderr=sys.stdout))

  def run(self, portlist):
    """
    This method launch the server and create all the controllers.
    It also launch all thread needed by paramiko and load the server private key.

    :portlist:
        this port list represent the controllers port.

      """
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

def run():
  """
  Entry point for the Server, it allow you to import and then run the server.
  This launch the server, bind it to the desired port and launch the controllers.
  """
  try:
    portlist = range(int(opts["controller_port"]), int(opts["controller_port"]) + int(opts["controller_number"]))
    if opts["debug"] == True:
            logging.basicConfig(level=logging.DEBUG)
    logging.debug("server is listenning port -> %s", int(opts["server_port"]))
    logging.debug("launching controlers -> %s", portlist)
    paramiko.util.log_to_file('sx4it_server.log')
    server = Server(int(opts["server_port"]))
    server.run(portlist)
  except Exception as e:
    print "Error !", e
    parser.print_help()
