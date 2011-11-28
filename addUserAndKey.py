#!/usr/bin/env python

from database import Session
from database.entity import *
import os

firstname = os.getenv('USER')
lastname = firstname
mail = firstname + '@sx4it.com'
password = firstname

def loadkey(key):
	b = open(os.path.expanduser(key)).read().split()[1]
	return b

key = loadkey('~/.ssh/id_rsa.pub')

user1 = user.User(firstname, lastname, mail, password)
user1.userkey = [userKey.UserKey(key, 'type')]

Session._userRequest.addUser(user1)
