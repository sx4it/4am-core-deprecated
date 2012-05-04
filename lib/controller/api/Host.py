"""
Manipulation of the host representations
"""

import logging
import traceback
from common.jsonrpc.call import Callable
from controller.server import Server
from database.entity import host, hostKey
import sys

@Callable
def add(*param, **dic):
    """
    We may need to think about the choice between hostname/ip.

    :hostkey:
    The remote host key in the form of a base64 encoded string
    """
    #Check if hostname already exist
    if dic.get("hostname") is None:
        return "No hostname given."

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

    try:
        host1 = Server.instance().db._hostRequest.getHostByHostname(dic.get("hostname"))
        if host1:
            return "%s already exist."%dic.get("hostname")
    except:
        return "ERROR => Failed to retrieve host %s: %s"%(dic.get("hostname"), sys.exc_info()[1])

#    try:
#        remoteKey = Server.instance().rE.getRemoteHostKey(dic.get("ip"), dic.get("port"), hostKeyType)
#    except:
#        logging.debug(traceback.print_exc())
#        raise RuntimeError('Connection KO') # FIXME: Raise a better error
#    if dic.get("hostkey") is not None and dic.get("hostkey") != remoteKey:
#        raise RuntimeError('Invalid key') # FIXME: Raise a better error
#    Server.instance().rE.addRemoteHostKey(dic.get("ip"), hostKeyType, remoteKey)

    # Add new host and his key in database
    host1 = host.Host(dic.get("hostname"), dic.get("ip"), dic.get("port"), dic.get("mgmtusername"))
    host1.hostKey = [hostKey.HostKey(dic.get("hostkey"), hostKeyType)]
    try:
        Server.instance().db._hostRequest.addHost(host1)
    except:
        return "ERROR => Failed to add %s: %s"%(dic.get("hostname"), sys.exc_info()[1])
    return "%s has been successfully added!"%dic.get("hostname")

@Callable
def addKey(*param, **dic):
    """
    Add a key and keyType to the given host
    """
    if dic.get("hostname") is None or dic.get("hostkey") is None or dic.get("hostkeytype") is None:
        return "All hostname, host key and key type must be given."
    try:
        host1 = Server.instance().db._hostRequest.getHostByHostname(dic.get("hostname"))
        if not host1:
            return "%s does not exist."%dic.get("hostname")
        host1.hostkey.append(hostKey.HostKey(dic.get("hostkey"), dic.get("hostkeytype")))
        Server.instance().db._hostRequest.addHost(host1)
    except:
        return "ERROR => Failed to add key to host %s: %s"%(dic.get("hostname"), sys.exc_info()[1])
    return "%s key's successfully added!"%dic.get("hostname")

@Callable
def delete(*param, **dic):
    """
    delete an host using the given hostname
    """
    if dic.get("hostname") is None:
        return "No hostname given."
    try:
        host1 = Server.instance().db._hostRequest.getHostByHostname(dic.get("hostname"))
        if not host1:
            return "%s does not exist."%dic.get("hostname")
        Server.instance().db._hostRequest.removeHost(host1)
    except:
        return "ERROR => Failed to delete host %s: %s"%(dic.get("hostname"), sys.exc_info()[1])
    return "%s has been successfully deleted!"%dic.get("hostname")

@Callable
def deleteKey(*param, **dic):
    """
    delete an hostkey using the given hostname and keyid
    """
    if dic.get("hostkey") is None:
        return "No hostname given."
    try:
#        key1 = Server.instance().db._
        host1 = Server.instance().db._hostRequest.getHostByHostname(dic.get("hostname"))
#        if not host1:
#            return "%s does not exist."%dic.get("hostname")
#        Server.instance().db._hostRequest.removeHost(09host1)
    except:
        return "ERROR => Failed to delete hostkey host %s: %s"%(dic.get("hostname"), sys.exc_info()[1])
    return "%s has been successfully deleted!"%dic.get("hostname")


@Callable
def update(*param, **dic):
    """
    Update an host
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
        return "ERROR => Failed to update host %s: %s"%(dic.get("hostname"), sys.exc_info()[1])
    return "%s has been updated!"%(hostname)

@Callable
def list(*param, **dic):
    """
    List all host
    """
    hosts = Server.instance().db._hostRequest.getAllHost()
    if not hosts:
        return "No host stored."
    return hosts

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
    return "Not implemented... yet."

@Callable
def getKeysFromHostame(*param, **dic):
    """
    Get all keys  associated to the given hostname
    """
    return "Not implemented... yet."

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

