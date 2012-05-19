"""
Manipulation of the user representations
"""

import logging
from sqlalchemy import orm
from common.jsonrpc.call import Callable
from controller.server import Server
from database.entity import user, userKey

from ControllerException import *

"""
TODO:
check existing keyname when adding
"""

@Callable
def add(*param, **dic):
  """
  Add a new user in database, also add a key if given
  """
  if dic.get("login") is None:
    raise MissingArgumentError("login")
  if dic.get("firstname") is None:
    raise MissingArgumentError("fistname")
  if dic.get("lastname") is None:
    raise MissingArgumentError("lastname")
  if dic.get("email") is None:
    raise MissingArgumentError("login")
  if dic.get("password") is None:
    raise MissingArgumentError("password")
  password = dic.get("password")
  usr = user.User(dic.get("login"), dic.get("firstname"), dic.get("lastname"), dic.get("email"), password)

  if dic.get("name") is not None and dic.get("key") is not None:
    usr.userkey = [userKey.UserKey(dic.get["name"], dic.get["key"], dic.get["type"], dic.get["detail"])]
  Server.instance().db._userRequest.addUser(usr)
  return True

@Callable
def addKey(*param, **dic):
  """
  Add a key and kink it to a user
  """
  if dic.get("login") is None or dic.get("name") is None or dic.get("key") is None:
    raise MissingArgumentError("requiere login, name and key")

  usr = Server.instance().db._hostRequest.getUser(dic.get("login"))
  usr.hostkey.append(hostKey.HostKey(dic.get["name"], dic.get["key"], dic.get["type"], dic.get["detail"]))
  Server.instance().db._hostRequest.addHost(usr)
  return True

@Callable
def delete(*param, **dic):
  """
  Delete a user
  """
  if dic.get("login") is None:
    raise MissingArgumentError("login")

  usr = Server.instance().db._userRequest.getUser(dic.get("login"))
  Server.instance().db._userRequest.deleteUser(usr)
  return True

@Callable
def list(*param, **dic):
  """
  Get a list of all user
  """
  usr = Server.instance().db._userRequest.getAllUser()
  return usr

@Callable
def get(*param, **dic):
  """
  Get a user
  """
  if dic.get("login") is None:
    raise MissingArgumentError("login")
  usr = Server.instance().db._userRequest.getUser(dic.get("login"))
  return usr

@Callable
def update(*param, **dic):
  """
  Update user's detail
  login can't be changed
  """
  if len(dic) < 2:
    raise MissingArgumentError("nothing to update")
  if dic.get("login") is None:
    raise MissingArgumentError("login")
  usr = Server.instance().db._userRequest.getUser(dic.get("login"))

  if dic.get("firstname") is not None:
    usr.firstname = dic.get("firstname")
  if dic.get("lastname") is not None:
    usr.lastname = dic.get("lastname")
  if dic.get("email") is not None:
    usr.email = dic.get("email")
  if dic.get("password") is not None:
    usr.password = dic.get("password")
  if dic.get("active") is not None:
    usr.active = dic.get("active")
  Server.instance().db._userRequest.addUser(usr)
  return True




#pourquoi cette fonction dans le controller?
@Callable
def checkPassFromUsername(*username, **dic):
  try:
    if dic.get("user") is None:
      return False
    user = dic.get("user")
    if dic.get("password") is None:
      return False
    password = dic.get("password")
    user = Server.instance().db._userRequest.getUser(user)
    if user.password == password:
      return True
  except : #TODO finaly ? FIXME BAAAAAA CATCH ALL
    return False
  return False

#Idem, pour dans le controller?
@Callable
def getKeyFromUsername(*username, **dic):
  if dic.get("user") is None:
    return ""
  user = dic.get("user")
  try:
    user = Server.instance().db._userRequest.getUser(user)
  except orm.exc.NoResultFound:
    #FIXME: Not found results are not really an exception++
    raise RuntimeError("{0} not found".format(user))
  if len(user.userkey) > 0:
    keys = user.userkey[0].key
  else:
    return ""
  logging.debug("getKeyFromUsername-> %s", keys)
  return keys

@Callable
def updateKey(*param, **dic):
  """
  Update key's detail
  """
  return "Not implemented... yet."
