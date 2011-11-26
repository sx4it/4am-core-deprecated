from sqlAlchemySession import SqlAlchemySession
from entity import *

sess = SqlAlchemySession('mysql://root:root@localhost/sx4it')

# test engine
sess._engine.execute("select 1").scalar()

user1 = user.User('toto', 'titi', 'tata', 'tutu')
sess._userRequest.addUser(user1)

id = user1.id

print sess._userRequest.getUserById(id)
sess._userRequest.removeUser(user1)
print sess._userRequest.getUserById(id)
