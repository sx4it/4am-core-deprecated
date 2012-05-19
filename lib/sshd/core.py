# -*- coding: utf-8 -*-
# Open Source Initiative OSI - The MIT License (MIT):Licensing
#
# The MIT License (MIT)
# Copyright (c) 2012 sx4it (contact@sx4it.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import paramiko
import sys
import os
import socket
import threading
import base64
import logging

from sshhandler import shell, sx4itsession

from common import *
from common.jsonrpc.zmqProxy import zmqREQServiceProxy
from common.jsonrpc.call import JRPCError

logger = logging.getLogger(__name__)

def Worker(client, host_key, ctl_addrs):
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
        session = sx4itsession.sx4itsession(chan, ctl_addrs)
      elif server.chan_name == 'session':
        print "making shell"
        session = shell.shell(chan, ctl_addrs)
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
      .. note:: we connect via zmq to check the userkey
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
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        """
        This function remotly check that the publickey is matching with the username.
        """
        try:
            userkey = Server.instance()._ctl_proxy.User.getKeyFromUsername(user=username)
        except JRPCError:
            pass
        else:
            if len(userkey) and key == paramiko.RSAKey(data=base64.decodestring(userkey)):
                return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        """
        This function is getting the two type of allowed loggin mode.
        """
        return 'publickey'

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
    def __init__(self):
        self.__configured = False

    def configure(self, addr, port, key_file, ctl_addrs):
        '''
        Server constructor.

        :key_file:
            file containing the private key of the ssh server
        :ctl_addrs:
            addresses of the controller, 0MQ format
        '''
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((addr, port))
        logger.info("Server is listenning on {0}:{1}".format(addr, port))
        self._sock.listen(100)
        self._host_key = paramiko.RSAKey(filename=key_file)
        self._thread = []
        self._ctl_addrs = ctl_addrs
        self.__configured = True
        #paramiko.util.log_to_file('sx4it_server.log')
    
    @staticmethod
    def instance():
        """
        Returns a global Server instance.
        """
        if not hasattr(Server, "_instance"):
            Server._instance = Server()
        return Server._instance

    @staticmethod
    def initialized():
        """
        Returns true if the singleton instance has been created.
        """
        return hasattr(Server, "_instance")

    def run(self):
        """
        This method launch the server and create all the controllers.
        It also launch all thread needed by paramiko and load the server private key.
        
        :portlist:
            this port list represent the controllers port.
        
          """
        if not self.__configured:
            raise RuntimeError("Can not start an unconfigured Server instance.")
        logger.info("Connecting to controlers {0}".format(self._ctl_addrs))
        self._ctl_proxy = zmqREQServiceProxy([addr for addr in self._ctl_addrs])
        try:
            while True:
                sclient, addr = self._sock.accept()
                logger.debug("New connection from {0}".format(addr))
                self._thread.append(threading.Thread(target=Worker,
                                            args=(sclient, self._host_key,
                                                    self._ctl_addrs)))
                # thread.append(multiprocessing.Process(target=Worker, args=(client, host_key)))
                # can't test with real thread... http://github.com/robey/paramiko/issues/27
                self._thread[-1].deamon = True
                self._thread[-1].start()
        except KeyboardInterrupt:
          map(lambda b : b.join(), self._thread)

