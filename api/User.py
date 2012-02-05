"""
test api for autocomplete generation
"""
from jsonrpc import call
import logging
import database
from database.entity import user

#TODO find a better way to do it
import sys
import ast
import json
opts = sys.argv[2]
opts = json.loads(opts)
db_session = database.InitSession(opts)

@call.Callable
def add(param1):
	""" api.add function !"""
	logging.debug("Add -> %s", param1)
	return True
@call.Callable
def delete(param1):
	""" api.delete function !"""
	logging.debug("delete -> %s", param1)
	return "Yeah it is delete !"
@call.Callable
def help():
	""" api.delete function !"""
	return "Yeah it is delete !"
@call.Callable
def deletee(param1):
	""" api.delete function !"""
	logging.debug("delete -> %s", param1)
	return "Yeah it is delete !"

@call.Callable
def checkPassFromUsername(username):
	user = db_session._userRequest.getUserByName(username[0][0])
	if user.password == username[0][1]:
		return True
	return False

@call.Callable
def getKeyFromUsername(username):
	logging.debug("getKeyFromUsername-> %s", username)
	username = username[0][0]
	user = db_session._userRequest.getUserByName(username)
	keys = user.userkey[0].ukkey
	logging.debug("getKeyFromUsername-> %s", keys)
	return keys
