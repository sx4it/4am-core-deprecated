## This a test API

from jsonrpc import Callable

# For Paramiko
import paramiko
import socket

import fabric.api
import fabric.network
import Server

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
def addUser(userToAdd, userToConnect, keyFile, hostname, port=22):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    # FIXME: We are only loading RSAKeys and not DSS
    key = paramiko.RSAKey.from_private_key_file(keyFile)
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
def reloadRemoteHostKeys(filename=None):
    if filename is None:
        filename = remoteHostKeysFile
    remoteHostKeys.clear()
    remoteHostKeys.load(filename)

@Callable
def addRSARemoteHostKey(hostname, key):
    '''TODO'''
    raise RuntimeError('Not Implemented')

@Callable
def delRSARemoteHostKey(hostname, key):
    '''TODO'''
    raise RuntimeError('Not Implemented')
    
@Callable
def addDSSRemoteHostKey(hostname, key):
    '''TODO'''
    raise RuntimeError('Not Implemented')

@Callable
def delDSSRemoteHostKey(hostname, key):
    '''TODO'''
    raise RuntimeError('Not Implemented')
