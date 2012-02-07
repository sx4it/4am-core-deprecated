"""
test api for autocomplete generation
"""
from jsonrpc import call
import logging
import database
from database.entity import user
from database.entity import userKey
import pprint
import StringIO

#TODO find a better way to do it
import sys
import ast
import json
opts = sys.argv[2]
opts = json.loads(opts)
db_session = database.InitSession(opts)

def pprinttable(rows):
	out = StringIO.StringIO()
	if len(rows) > 1:
		headers = rows[0]
		lens = []
		for i in range(len(rows[0])):
			lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
		formats = []
		hformats = []
		for i in range(len(rows[0])):
			if isinstance(rows[0][i], int):
				formats.append("%%%dd" % lens[i])
			else:
				formats.append("%%-%ds" % lens[i])
			hformats.append("%%-%ds" % lens[i])
		pattern = " | ".join(formats)
		hpattern = " | ".join(hformats)
		separator = "-+-".join(['-' * n for n in lens])
		print >> out, hpattern % tuple(headers)
		print >> out, separator
		for line in rows:
			print >> out, pattern % tuple(line)
	elif len(rows) == 1:
		row = rows[0]
		hwidth = len(max(row,key=lambda x: len(x)))
		for i in range(len(row)):
			print >> out, "%*s = %s" % (hwidth,row[i],row[i])
	return out.getvalue()


@call.Callable
def list(*param, **dic):
	"""
	api.list list all users
	"""
	users = db_session._userRequest.getAllUser()
	s = StringIO.StringIO()
	tab = [("id", "firtname", "lastname", "email")]
	for b in users:
		tab.append((str(b.id), b.firstname, b.lastname, b.email))
	return pprinttable(tab)

@call.Callable
def add(*param, **dic):
	"""
	api.add a new user in database

	name = username
	group = usergroup
	return true if everything is ok :)
	"""
	if dic.get("firstname") is None:
		return "No firstname given"
	firstname = dic.get("firstname")
	if dic.get("lastname") is None:
		return "No lastname given"
	lastname = dic.get("lastname")
	if dic.get("email") is None:
		return "No user email given"
	email = dic.get("email")
	if dic.get("password") is None:
		return "No user password given"
	password = dic.get("password")
	user1 = user.User(firstname, lastname, email, password)
	if dic.get("key") is not None:
		user1.userkey = [userKey.UserKey(dic["key"], 'type')] # Add key if he gave one
	if db_session._userRequest.addUser(user1) == True:
		return True
	return False

@call.Callable
def delete(*param, **dic):
	"""
	User.delete [name=USERNAME]
	"""
	if dic.get("firstname") is None:
		return "No firstname given"
	firstname = dic.get("firstname")
	try:
		user = db_session._userRequest.getUserByName(firstname)
	except:
		return "%s cannot be delete."%firstname
	if db_session._userRequest.removeUser(user):
		return True
	return "%s cannot be delete."%firstname


	name = dic.get("name")
	if name is None:
		return delete.__doc__
	return "%s has been delete !"%(name)

@call.Callable
def checkPassFromUsername(*username, **dic):
	try:
		if dic.get("user") is None:
			return False
		user = dic.get("user")
		if dic.get("password") is None:
			return False
		password = dic.get("password")
		user = db_session._userRequest.getUserByName(user)
		if user.password == password:
			return True
	except : #TODO finaly ?
		return False
	return False

@call.Callable
def getKeyFromUsername(*username, **dic):
	if dic.get("user") is None:
		return ""
	user = dic.get("user")
	try:
		user = db_session._userRequest.getUserByName(user)
		keys = user.userkey[0].ukkey
		logging.debug("getKeyFromUsername-> %s", keys)
		return keys
	except :
		return ""
