'''
Manipulation of the host representations
'''

import logging
import traceback
from common.jsonrpc.call import Callable
from controller.server import Server

@Callable
def add(name=None, ip=None, port=22, HostKey=None, HostKeyType=None, tpl=None):
    '''
    We may need to think about the choice between hostname/ip.

    :HostKey:
        The remote host key in the form of a base64 encoded string
    '''
    if name is None or ip is None:
        raise RuntimeError('Invalide arg') # FIXME: Raise a better error
    if HostKeyType is not None:
        # FIXME: check if this is a correct type (policy...)
        pass
    else:
         #FIXME: Need to be in the policy
        HostKeyType = 'ssh-rsa'
    if HostKey is None: # FIXME: strict policy may require HostKey to be present
        pass
    try:
        remoteKey = Server.instance().rE.getRemoteHostKey(ip, port, HostKeyType)
    except:
        logging.debug(traceback.print_exc())
        raise RuntimeError('Connection KO') # FIXME: Raise a better error
    if HostKey is not None and HostKey != remoteKey:
        raise RuntimeError('Invalid key') # FIXME: Raise a better error
    Server.instance().rE.addRemoteHostKey(ip, HostKeyType, remoteKey)
    return True
    # Insert remoteKey in the database

#@Callable
#def takeControl(hostname=None, username=None, password=None, policy='default')
#    '''
#    Create a dedicated user on the remote host for management purposes and apply the default policy.
#    '''
#    if username is None:
#        username = 'root' #FIXME: get from policy
#    mgmtUserName = '4ammgmt' #FIXME: get from policy/template whatever
#    if username != mgmtUserName:
#        cmd = 'adduser --system --force-badname --home /opt/4am/ --shell /bin/bash --disabled-password --create-home ' + mgmtUserName
#        Server.instance().rE.cmdExec(ip, HostKeyType, remoteKey)
#    # FIXME: apply policy
    
