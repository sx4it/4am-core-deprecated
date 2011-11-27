from session import Session
from entity import *

# test engine
Session._engine.execute("select 1").scalar()

user1 = user.User('toto', 'titi', 'tata', 'tutu')
Session._userRequest.addUser(user1)

id = user1.id

print Session._session.new

print Session._userRequest.getUserById(id)
#Session._userRequest.removeUser(user1)
Session._userRequest.removeUserById(id)
#print Session._userRequest.getUserById(id)


