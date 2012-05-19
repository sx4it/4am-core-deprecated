# -*- coding: utf-8 -*-
# Open Source Initiative OSI - The MIT License (MIT):Licensing
#
# The MIT License (MIT)
# Copyright (c) 2012 sx4it (contact@sx4it.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sys
import logging
import traceback
import sqlalchemy 

from common.jsonrpc.call import Callable
from controller.server import Server
from database.entity import host, hostKey

logger = logging.getLogger(__name__)

class HostError(Exception):
    """Base class for errors in the api.host package."""

@Callable
def add(name=None, ip=None, port=22, hostKey=None, hostKeyType=None, tpl=None):
    '''
    We may need to think about the choice between hostname/ip.

    :hostkey:
    The remote host key in the form of a base64 encoded string
    '''
    if name is None:
        raise HostError('No hostname given.')
    # Check if host already exist in the database
    try:
        host1 = Server.instance().db._hostRequest.getHostByHostname(name)
        if host1:
            raise HostError("{0} already exist.".format(name)) # FIXME: Raise a better error
    except (sqlalchemy.exc.SQLAlchemyError, sqlalchemy.exc.InvalidRequestError): #FIXME: What do we except ?
        logger.error(sys.exc_info()[1])
        raise HostError("Failed to retrieve host {0}.".format(name)) # FIXME: Raise a better error
    if HostKey is None: # FIXME: strict policy may require HostKey to be present
        pass
    try:
        remoteKey = Server.instance().rE.getRemoteHostKey(ip, port, HostKeyType)
    except: #FIXME: What do we except ?
        logger.info(traceback.print_exc())
        raise RuntimeError('Connection KO') # FIXME: Raise a better error and catch different type of exception
    if HostKey is not None and HostKey != remoteKey:
        raise RuntimeError('Invalid key') # FIXME: Raise a better error
    Server.instance().rE.addRemoteHostKey(ip, HostKeyType, remoteKey)
    return True
    # Insert remoteKey in the database
    mgmtusername = '4am' #FIXME: in policy
    # Add new host and his key in database
    host1 = host.Host(name, ip, port, mgmtusername)
    host1.hostKey = [hostKey.HostKey(hostKey, hostKeyType)]
    try:
        Server.instance().db._hostRequest.addHost(host1) # FIXME : What happen if one of the insert request fails ? Are both request canceled ? #transaction ?
    except: #FIXME: What do we except ?
        logger.error("Failed to add host {0} details :\n".format(name, sys.exc_info()[1]))
        raise RuntimeError("Failed to add host {0}.".format(name)) # FIXME: Raise a better error
    return True # We should maybe return a kind of object representing the host

@Callable
def add_key(name=None, hostkey=None, hostkeytype=None):
    """
    Add a key and keyType to the given host
    """
    if name is None or hostkey is None or hostkeytype is None:
        raise RuntimeError('Name, host key and key type must be given.') # FIXME: Raise a better error
    try:
        host1 = Server.instance().db._hostRequest.getHostByHostname(name)
        if not host1:
            raise RuntimeError("{0} does not exist.".format(name)) # FIXME: Raise a better error
        host1.hostkey.append(hostKey.HostKey(hostkey), hostkeytype)
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
def delete_key(*param, **dic):
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
def get_host(*param, **dic):
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
def get_host_from_key(*param, **dic):
    """
    Get an Host from the given key
    """
    return "Not implemented... yet."

@Callable
def get_keys_from_hostame(*param, **dic):
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
    
