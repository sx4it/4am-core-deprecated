#!/usr/bin/env python

from database import Session
#from database import entity
from database.entity import *

# test engine
Session._engine.execute("select 1").scalar()

user1 = user.User('toto', 'titi', 'tata', 'tutu')
Session._userRequest.addUser(user1)

key1 = userKey.UserKey('keyname', 'keytype')
user1.userkey = [key1]
Session._userRequest.addUser(user1)

id = user1.id

user = Session._userRequest.getUserById(id)
print user.firstname

#Session._userRequest.removeUser(user1)
#Session._userRequest.removeUserById(id)
#print Session._userRequest.getUserById(id)


