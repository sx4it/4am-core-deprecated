'''
Manipulation of the host representations
'''

import logging
import traceback
import StringIO
from common.jsonrpc.call import Callable
from controller.server import Server
from database.entity import host, hostKey
from User import pprinttable

@Callable
def add(*param, **dic):
    '''
    We may need to think about the choice between hostname/ip.

    :hostkey:
        The remote host key in the form of a base64 encoded string
    '''

    if dic.get("ip") is None or dic.get("port") is None:
        return "Ip and port of the host must be given."
    if dic.get("hostkey") is None: # FIXME: strict policy may require HostKey to be present
        return "An hostKey must be given."
    if dic.get("hostkeytype") is not None:
        # FIXME: check if this is a correct type (policy...)
        hostKeyType = dic.get("hostkeytype")
        pass
    else:
         #FIXME: Need to be in the policy
        hostKeyType = 'ssh-rsa'

    #Check if hostname already exist
    if dic.get("hostname") is None:
        return "No hostname given."
    try:
        host = Server.instance().db._hostRequest.getHostByHostname(dic.get("hostname"))
        if host:
            return "%s already exist."%dic.get("hostname")
    except:
        return "ERROR: %s cannot check existing hostname."%dic.get("hostname")

#    try:
#        remoteKey = Server.instance().rE.getRemoteHostKey(dic.get("ip"), dic.get("port"), hostKeyType)
#    except:
#        logging.debug(traceback.print_exc())
#        raise RuntimeError('Connection KO') # FIXME: Raise a better error
#    if dic.get("hostkey") is not None and dic.get("hostkey") != remoteKey:
#        raise RuntimeError('Invalid key') # FIXME: Raise a better error
#    Server.instance().rE.addRemoteHostKey(dic.get("ip"), hostKeyType, remoteKey)

    # Add new host and his key in database
    host = host.Host(dic.get("hostname"), dic.get("ip"), dic.get("port"), dic.get("mgmtusername"))
    try:
        host.hostKey = [hostKey.HostKey(dic.get("hostkey"), hostKeyType)]
        Server.instance().db._hostRequest.addHost(user)
    except:
        return "ERROR: %s failed to be added."%dic.get("hostname")
    return "%s has been successfully added!"%dic.get("hostname")

@Callable
def addKeyToHost(*param, **dic):
    """
    Add a key and keyType to the given host
    """
    if dic.get("hostname") is None or dic.get("hkkey") is None or dic.get("hktype") is None:
        return "All hostname, host key and key type must be given."
    try:
        host = Server.instance().db._hostRequest.getHostByHostname(hostname)
        if not host:
            return "%s does not exist."%hostname
        host.hostKey.append(hostKey.HostKey(dic.get("hkkey"), dic.get("hktype")))
        Server.instance().db._hostRequest.addHost(host)
    except:
        return "ERROR: %s key's failed to be updated."%hostname
    return "%s key's successfully added!"%hostname

@Callable
def delete(*param, **dic):
    """
    delete an host using the given hostname
    """
    if dic.get("hostname") is None:
        return "No hostname given."
    hostname = dic.get("hostname")
    try:
        host = Server.instance().db._hostRequest.getHostByHostname(hostname)
        if not host:
            return "%s does not exist."%hostname
        Server.instance().db._hostRequest.removeHost(host)
    except:
        return "ERROR: %s cannot be delete."%hostname
    return "%s has been successfully delete!"%(hostname)

def update(*param, **dic):
    """
    update an host
    """
    if dic.get("hostname") is None:
        return "No hostname given."
    hostname = dic.get("hostname")
    try:
        host = Server.instance().db._hostRequest.getHostByHostname(hostname)
        if not host:
            return "%s does not exist."%hostname
        if dic.get("ip") is not None:
            host.ip = dic.get("ip")
        if dic.get("port") is not None:
            host.ip = dic.get("port")
        if dic.get("mgmtusername") is not None:
            host.ip = dic.get("mgmtusername")
        Server.instance().db._hostRequest.addHost(host)
    except:
        return "ERROR: %s failed to be updated."%hostname
    return "%s has been updated!"%(hostname)

@Callable
def list(*param, **dic):
    """
    List all host
    """
    hosts = Server.instance().db._hostRequest.getAllHost()
    if not hosts:
        return "No host stored."
    s = StringIO.StringIO()
    tab = [("ip", "hostname", "port", "mgmtusername")]
    for b in hosts:
        tab.append((str(b.ip), b.hostname, b.port, b.mgmtusername))
    return pprinttable(tab)

@Callable
def getHost(*param, **dic):
    """
    Get an Host from the given hostname
    """
    if dic.get("hostname") is None:
        return "No hostname given."
    hostname = dic.get("hostname")
    try:
        host = Server.instance().db._hostRequest.getHostByHostname(hostname)
        if not host:
            return "%s does not exist."%hostname
    except:
        return "ERROR: %s cannot be retrieve."%hostname
    return "Hostname: %s, Ip:%s, Port:%s"%(hostname, host.ip, host.port)

@Callable
def getHostFromKey(*param, **dic):
    """
    Get an Host from the given key
    """
    print "Not implemented... yet."

@Callable
def getKeysFromHostame(*param, **dic):
    """
    Get all keys  associated to the given hostname
    """
    print "Not implemented... yet."

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

