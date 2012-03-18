#!/usr/bin/env python

import paramiko
import json
import socket
import logging
import unittest
from common.jsonrpc import proxy, call
import os, sys

from optparse import OptionParser

logging.basicConfig(level=logging.CRITICAL)

parser = OptionParser()
parser.add_option("-p", "--port", dest="port", type="int",
                  help="port of the client", metavar="PORT", default=2200)
parser.add_option("-a", "--addr", dest="ip",
                  help="ip of the client", metavar="IP_ADDRESS", default="127.0.0.1")


class Client(proxy.Proxy):
  def __init__(self, **option):
    super(Client, self).__init__()
    self.client = paramiko.SSHClient()
    self.client.load_system_host_keys()
    #po = paramiko.WarningPolicy()
    po = paramiko.MissingHostKeyPolicy()
    self.client.set_missing_host_key_policy(po)
    self.client.connect(option['host'], option['port'], option['user'])
    self.chan = self.client.get_transport().open_channel('sx4it_command')
  def __call__(self, *args, **kwargs):
# put an id into jsonrpc requests
    postdata = super(Client, self).__call__(*args, **kwargs)
    self.chan.send(postdata + "\r")
    res = self.chan.recv(2048)
    logging.debug('recieving %s', res)
    return call.analyzeJRPCRes(res)



(options, args) = parser.parse_args()
logging.basicConfig(level=logging.DEBUG)

class unitTest(unittest.TestCase):
  client = Client(host=options.ip, port=options.port, user=os.getenv('USER'))
  def testUser0AddCommand(self):
    """
    testing Add User Command
    """
    self.assertEqual(self.client.User.add(firstname='toto'), "No lastname given")
    self.assertEqual(self.client.User.add(firstname='toto', password='123456', lastname="wooo", email="toto@gmail.com"), True)
    #Adding the same user should be false
    self.assertEqual(self.client.User.add(firstname='toto', password='123456', lastname="wooo", email="toto@gmail.com"), False)
    self.assertEqual(self.client.User.add(firstname='tata', password='123456', lastname="wooo", email="toto@gmail.com"), True)
    self.assertEqual(self.client.User.add(firstname='user_with_key', password='123456', lastname="wooo", email="toto@gmail.com", key="$$$$$$$$$$"), True)
  def testUser1List(self):
    """
    testing List User Command
    """
    self.assertIn("toto" ,self.client.User.list())
  def testUser2checkPassFromUsername(self):
    """
    testing List User Command
    """
    self.assertEqual(self.client.User.checkPassFromUsername(user = "toto", password= "123456"), True)
    self.assertEqual(self.client.User.checkPassFromUsername(user = "toto", password= "123457"), False)
    self.assertEqual(self.client.User.checkPassFromUsername(user = "toto", password= ""), False)
    self.assertEqual(self.client.User.checkPassFromUsername(user = "toto", password= "12345"), False)
    self.assertEqual(self.client.User.checkPassFromUsername(user = "toto"), False)
    self.assertEqual(self.client.User.checkPassFromUsername(), False)
  def testUser3getKeyFromUsername(self):
    """
    testing List User Command
    """
    self.assertEqual(self.client.User.getKeyFromUsername(user = "toto"), "")
    self.assertEqual(self.client.User.getKeyFromUsername(user = "user_with_key"), "$$$$$$$$$$")
  def testUser4DelCommand(self):
    """
    testing Del User Command
    """
    self.assertEqual(self.client.User.delete(firstname='t'), "t cannot be delete.")
    self.assertEqual(self.client.User.delete(firstname='toto'), True)
    self.assertEqual(self.client.User.delete(firstname='tata'), True)
    self.assertEqual(self.client.User.delete(firstname='user_with_key'), True)
  def testBadFunctionName(self):
    """
    testing failure with bad function name
    """
    self.assertRaises(call.JRPCError, self.client.User.WtfFunction, "t", "w")
    self.assertRaises(call.JRPCError, self.client.Wtf.add, "t", "w")
    self.assertRaises(call.JRPCError, self.client.Wt, "t", "w")
    self.assertRaises(call.JRPCError, self.client.Wt)
    self.assertRaises(call.JRPCError, self.client.Wtf, bo="woi")
  #TODO Add more stuff (and not only test Proxy)

if __name__ == "__main__":
  unittest.main()
