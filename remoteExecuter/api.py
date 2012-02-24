## This a test API

from call import Callable

# For Paramiko
import paramiko
import socket

import fabric.api
import fabric.network
import Server
import base64

fabric.api.env.no_agent = True
fabric.api.env.reject_unknown_hosts = True
fabric.api.env.abort_on_prompts = True

def verifyKey(hostname, key):
    '''Key is a Pkey paramiko file'''
    if remoteHostKeys.check(hostname, key) is not True:
        raise RuntimeError('The key is not associated with this host')

@Callable
def getRemoteHostKey(hostname, port=22, key_type='ssh-rsa'):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    secopt = t.get_security_options()
    secopt._set_key_types([key_type])
    t.start_client()
    res = t.get_remote_server_key().get_base64()
    t.close()
    del t
    return res

@Callable
def addUser(userToAdd, userToConnect, key, hostname, port=22):
    if keytype == 'ssh-rsa': 
        key = paramiko.RSAKey(data=base64.decodestring(key)) 
    elif keytype == 'ssh-dss': 
        key = paramiko.DSSKey(data=base64.decodestring(key)) 
    else:
        raise RuntimeError('Invalid key type.')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    # FIXME: The remote key type is hard coded
    t.connect(hostkey=Server.remoteHostKeys[hostname]['ssh-rsa'], username=userToConnect, pkey=key)
    chan = t.open_session() 
    chan.set_combine_stderr(True)
    ## FIXME: We should make some check to prevent shell command injection
    chan.exec_command("useradd -m {0}".format(userToAdd)) 
    chan.shutdown_write()
    res = ''
    while True:
        buf = chan.recv(4096)
        if len(buf) is 0:
            break
        res += buf
    status = chan.recv_exit_status()
    if status is not 0:
        raise RuntimeError({ 'status': status, 'output': res })
    chan.close()
    t.close()
    return res


@Callable
def addUserFab(userToAdd, userToConnect, keyFile, hostname, port=22):
    '''On debian '''
    fabric.api.env.host_string = hostname + ':' + str(port)
    fabric.api.env.user = userToConnect
    fabric.api.env.key_filename = keyFile
    return fabric.api.run()

@Callable
def delUserFab(userToDel, userToConnect, keyFile, hostname, port=22):
    '''On debian '''
    fabric.api.env.host_string = hostname + ':' + str(port)
    fabric.api.env.user = userToConnect
    fabric.api.env.key_filename = keyFile
    ## We should make some check to prevent shell command injection
    return fabric.api.run("deluser --backup --quiet --remove-home {0}".format(userToDel))


@Callable
def reloadRemoteHostKeysFromFile(filename=None):
    '''Can be useful for debugging'''
    if filename is None:
        filename = Server.remoteHostKeysFile
    Server.remoteHostKeys.clear()
    Server.remoteHostKeys.load(filename)

@Callable
def addRemoteHostKey(hostname, keytype, key):
    '''
    Some day whe should also add ECDSA key
    '''
    if keytype == 'ssh-rsa': 
        key = paramiko.RSAKey(data=base64.decodestring(key)) 
    elif keytype == 'ssh-dss': 
        key = paramiko.DSSKey(data=base64.decodestring(key)) 
    else:
        raise RuntimeError('Invalid key type.')
    Server.remoteHostKeys.add(hostname, keytype, key)
    return True

@Callable
def delRemoteHostKey(hostname):
    '''
    Paramiko implementation of the HostKeys object seems buggy.
    del is not implemented on the dictionnary abstraction.
    It seems that it's mandatory to manipulate directly the _entries var.
    '''
    i = 0
    for e in Server.remoteHostKeys._entries: 
        if (hostname in e.hostnames):
            Server.remoteHostKeys._entries.pop(i)
            break
        i += 1
    return True
    
@Callable
def dumpRemoteHostKey():
    '''Debug function'''
    for i in Server.remoteHostKeys:
        print i, Server.remoteHostKeys[i]
    return True
