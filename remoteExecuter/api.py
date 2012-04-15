## This a test API


# For Paramiko
import paramiko
import socket
import base64

from remoteExecuter.server import Server
from common.jsonrpc.call import Callable


def verifyKey(hostname, key):
    '''Key is a Pkey paramiko file'''
    if remoteHostKeys.check(hostname, key) is not True:
        raise RuntimeError('The key is not associated with this host')

@Callable
def getRemoteHostKey(hostname, port, key_type):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, int(port)))
    t = paramiko.Transport(sock)
    secopt = t.get_security_options()
    secopt._set_key_types([key_type])
    t.start_client()
    res = t.get_remote_server_key().get_base64()
    t.close()
    del t
    return res

@Callable
def cmdExec(cmd, userToConnect, hostname, pkey, port, remoteKeyType, authKeyType):
    if authKeyType == 'ssh-rsa': 
        pkey = paramiko.RSAKey(data=base64.decodestring(pkey)) 
    elif authKeyType == 'ssh-dss': 
        pkey = paramiko.DSSKey(data=base64.decodestring(pkey)) 
    else:
        raise RuntimeError('Invalid key type.')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, port))
    t = paramiko.Transport(sock)
    # FIXME: The remote key type is hard coded
    t.connect(hostkey=Server.instance().remoteHostKeys[hostname][remotekeyType], username=userToConnect, pkey=pkey)
    chan = t.open_session() 
    chan.set_combine_stderr(True)
    chan.exec_command(cmd) 
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

try:
    import fabric.api
    import fabric.network
    fabric.api.env.no_agent = True
    fabric.api.env.reject_unknown_hosts = True
    fabric.api.env.abort_on_prompts = True

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

except:
    print 'No fabric support'


@Callable
def reloadRemoteHostKeysFromFile(filename=None):
    '''Can be useful for debugging'''
    if filename is None:
        filename = Server.instance().remoteHostKeysFile
    Server.instance().remoteHostKeys.clear()
    Server.instance().remoteHostKeys.load(filename)

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
    Server.instance().remoteHostKeys.add(hostname, keytype, key)
    return True

@Callable
def delRemoteHostKey(hostname):
    '''
    Paramiko implementation of the HostKeys object seems buggy.
    del is not implemented on the dictionnary abstraction.
    It seems that it's mandatory to manipulate directly the _entries var.
    '''
    i = 0
    for e in Server.instance().remoteHostKeys._entries: 
        if (hostname in e.hostnames):
            Server.instance().remoteHostKeys._entries.pop(i)
            break
        i += 1
    return True
    
@Callable
def dumpRemoteHostKey():
    '''Debug function'''
    for i in Server.instance().remoteHostKeys:
        print i, Server.instance().remoteHostKeys[i]
    return True
