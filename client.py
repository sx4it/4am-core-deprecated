#!/usr/bin/env python

import paramiko
import json
import socket
import logging
import unittest
import base64
from common.jsonrpc import proxy, call
import os, sys

from optparse import OptionParser

parser = OptionParser()
parser.add_option("", "--user-key", dest="user_key",
                  help="client private key path", metavar="USER_KEY_PATH", default="~/.ssh/id_rsa")
parser.add_option("-p", "--port", dest="port", type="int",
                  help="port of the client", metavar="PORT", default=2200)
parser.add_option("-a", "--addr", dest="ip",
                  help="ip of the client", metavar="IP_ADDRESS", default="127.0.0.1")

def loadkey(key):
  return paramiko.RSAKey(filename=key)

class Client:
  def __init__(self, **option):
    self.client = paramiko.SSHClient()
    self.client.load_system_host_keys()
    #po = paramiko.WarningPolicy()  Keep that ?
    po = paramiko.MissingHostKeyPolicy()
    self.client.set_missing_host_key_policy(po)
    self.client.connect(option['host'], option['port'], option['user'], pkey=loadkey(os.path.expanduser(option['key_path'])))
    self.chan = self.client.get_transport().open_channel('sx4it_command')
  def __call__(self, args):
# put an id into jsonrpc requests
    params = []
    if len(args) == 0:
      raise RuntimeError("Please give at least function name !")
    elif len(args) > 1:
      params = args[1:]
    out = {}
    for b in params:
      b = b.split("=")
      if len(b) != 2:
        out = params
        break
      out[b[0]] = b[1]
    if args[0].find('.') == -1:
      args[0] = args[0] + "." + args[0]
    postdata = call.forgeJRPC(args[0], 'jsonrpc', out)
    self.chan.send(postdata + "\r")
    res = self.chan.recv(2048)
    logging.debug('recieving %s', res)
    return call.analyzeJRPCRes(res)

if __name__ == "__main__":
  #logging.basicConfig(level=logging.DEBUG)
  try:
    (options, args) = parser.parse_args()
    client = Client(host=options.ip, port=options.port, user=os.getenv('USER'), key_path=options.user_key)
    print client(args)
  except call.JRPCError as error:
    print "Fatal Error:"
    print error
  except RuntimeError as e:
    print "Error:", e
  except paramiko.AuthenticationException as e:
    print "Error:", e
  except socket.error as e:
    print "Error:", e, "[" + options.ip + "]:", options.port
