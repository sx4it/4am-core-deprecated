#!/usr/bin/env python

import paramiko
import json
import socket
import logging
import unittest
from jsonrpc import proxy, call
import os, sys

from optparse import OptionParser

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
		po = paramiko.WarningPolicy()
		self.client.set_missing_host_key_policy(po)
		self.client.connect(option['host'], option['port'], option['user'])
		self.chan = self.client.get_transport().open_channel('sx4it_command')
	def __call__(self, *args, **kwargs):
# put an id into jsonrpc requests
		postdata = super(Client, self).__call__(args, kwargs)
		self.chan.send(postdata + "\r")
		res = self.chan.recv(2048)
		logging.debug('recieving %s', res)
		return call.analyzeJRPCRes(res)



class unitTest(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		(options, args) = parser.parse_args()
		logging.basicConfig(level=logging.DEBUG)
		self.client = Client(host=options.ip, port=options.port, user=os.getenv('USER'))
	def testUserCommand(self):
		self.assertTrue(self.client.User.add(name='toto', passwd='123456'))
		self.assertTrue(self.client.User.delete(name='toto'))
		self.assertTrue(self.client.User.deletee('t', 'w'))
	def testBadFunctionName(self):
		#testing failure with bad function name
		self.assertRaises(call.JRPCError, self.client.User.WtfFunction, "t", "w")
		self.assertRaises(call.JRPCError, self.client.Wtf.add, "t", "w")
		self.assertRaises(call.JRPCError, self.client.Wt, "t", "w")
		self.assertRaises(call.JRPCError, self.client.Wt)
		self.assertRaises(call.JRPCError, self.client.Wtf, bo="woi")
	#TODO Add more stuff (and not only test Proxy)

if __name__ == "__main__":
	logging.basicConfig(level=logging.CRITICAL)
	unittest.main()
