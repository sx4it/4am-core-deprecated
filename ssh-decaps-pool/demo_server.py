#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

import base64
from binascii import hexlify
import getpass
import os
import socket
import sys
import threading
import traceback

import paramiko
import select
import zmq
import signal
from Crypto import Random


# setup logging
paramiko.util.log_to_file('demo_server.log')

host_key = paramiko.RSAKey(filename='test_rsa.key')
#host_key = paramiko.DSSKey(filename='test_dss.key')

print 'Read key: {0}'.format(hexlify(host_key.get_fingerprint()))


class Server (paramiko.ServerInterface):
    # 'data' is the output of base64.encodestring(str(key))
    # (using the "user_rsa_key" files)
    f = open(os.path.expanduser('~/my_dss'), 'r') 
    data = f.read()
    f.close() 
    print data
    good_pub_key = paramiko.RSAKey(data=base64.decodestring(data))

    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        print 'Auth attempt with key: ' + hexlify(key.get_fingerprint())
        if (username == 'yann') and (key == self.good_pub_key):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth,
                                  pixelheight, modes):
        return True

#class paramiko1Client (object):
#    def __init__(self):
#        """
#        Create a new SSHClient.
#        """
#        self._system_host_keys = HostKeys()
#        self._host_keys = HostKeys()
#        self._host_keys_filename = None
#        self._log_channel = None
#        self._policy = RejectPolicy()
#        self._transport = None
#        self._agent = None

#def paramiko1_connect():
#    hostname = '10.211.55.8'
#    username = ''
#    try:
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.connect((hostname, 22))
#    except Exception, e:
#        print '*** Connect failed: ' + str(e)
#        traceback.print_exc()
#        sys.exit(1)
#    try:
#        t = paramiko.Transport(sock)
#        try:
#            t.start_client()
#        except paramiko.SSHException:
#            print '*** SSH negotiation failed.'
#            sys.exit(1)
#        try:
#            keys = paramiko.util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
#        except IOError:
#            try:
#                keys = paramiko.util.load_host_keys(os.path.expanduser('~/ssh/known_hosts'))
#            except IOError:
#                print '*** Unable to open host keys file'
#                keys = {}
#        # check server's host key -- this is important.
#        key = t.get_remote_server_key()
#        if not keys.has_key(hostname):
#            print '*** WARNING: Unknown host key!'
#        elif not keys[hostname].has_key(key.get_name()):
#            print '*** WARNING: Unknown host key!'
#        elif keys[hostname][key.get_name()] != key:
#            print '*** WARNING: Host key has changed!!!'
#            sys.exit(1)
#        else:
#            print '*** Host key OK.'
#        # get username
#        if username == '':
#            username = getpass.getuser()
#        if not t.is_authenticated():
#            path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
#            key = paramiko.RSAKey.from_private_key_file(path)
#            t.auth_publickey(username, key)
#        if not t.is_authenticated():
#            print '*** Authentication failed. :('
#            t.close()
#            sys.exit(1)
#        chan = t.open_session()
#        chan.get_pty()
#        chan.invoke_shell()
#        print 'Connected to paramiko1.'
#        return chan
#    except Exception, e:
#        print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
#        traceback.print_exc()
#        try:
#            t.close()
#        except:
#            pass
#        sys.exit(1)

def HandleClient():
	try:
	    context = zmq.Context()
	    zmqsocket = context.socket(zmq.REQ)
	    zmqsocket.connect("tcp://127.0.0.1:5000")
	    t = paramiko.Transport(client)
	    try:
		t.load_server_moduli()
	    except:
		print '(Failed to load moduli -- gex will be unsupported.)'
		raise
	    t.add_server_key(host_key)
	    server = Server()
	    try:
		t.start_server(server=server)
	    except paramiko.SSHException, x:
		print '*** SSH negotiation failed.'
		sys.exit(1)

	    # wait for auth
	    chan = t.accept(20)
	    if chan is None:
		print '*** No channel.'
		sys.exit(1)
	    print 'Authenticated!'

	    server.event.wait(10)
	    if not server.event.isSet():
		print '*** Client never asked for a shell.'
		sys.exit(1)

	    chan.send('Forwarding decapsulated traffic...')
	    while True:
		x = chan.recv(1024)
		if len(x) == 0:
			break
		zmqsocket.send(x)
		zmqsocket.recv()
	    chan.close()

	except Exception, e:
	    print '*** Caught exception: ' + str(e.__class__) + ': ' + str(e)
	    traceback.print_exc()
	    try:
		t.close()
	    except:
		pass
	    sys.exit(1)


#hostname = '10.211.55.8'
#client = paramiko.SSHClient()
#client.load_system_host_keys()
#path = os.path.join(os.environ['HOME'], '.ssh', 'id_rsa')
#client.connect(hostname, key_filename=path)
#desttrans = client.get_transport()
#destchan = desttrans.open_session()
#destchan.get_pty()
#destchan.invoke_shell()
#destchan = paramiko1_connect()
#

def sigchldHandler(sig, frame):
	deadChildPid, status = os.wait()
	print '{0!s} subprocess exited.'.format(deadChildPid)

gl_childlist = [ ]
run = True
# now connect
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 2200))
    sock.listen(100)
    signal.signal(signal.SIGCHLD, sigchldHandler)
    signal.siginterrupt(signal.SIGINT, True)
    print 'Listening for connection ...'
except Exception, e:
    print '*** Bind/listen failed: ' + str(e)
    traceback.print_exc()
    sys.exit(1)

while run:
	try:
		client, addr = sock.accept()
		print 'Got a connection from {0} !'.format(addr)
		try:
			pid = os.fork()
			if pid == 0:
				sock.close()
				Random.atfork()
				HandleClient()
                                run = False
			else:
				print 'Created a new forked process with pid {0!s}.'.format(pid)
		except OSError, e:
			print '*** Fork failed: ' + str(e)
			traceback.print_exc()
	except socket.error, e:
		if e.errno == 4:
			print 'WARNING: accept interrupted.'
		else:
			raise e
	except Exception, e:
		print 'ERROR: accept failed: ' + str(e)
		traceback.print_exc()


