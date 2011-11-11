import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

print sqlalchemy.__version__ 

# Create engine
engine = create_engine('mysql://root:root@localhost/sx4it', echo=True)

# test engine
engine.execute("select 1").scalar()

# Get base
Base = declarative_base()

## import Table

# Auto create all table in db if not exist
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

# Get a working session
session = Session()

import sys

sys.path.append('./entity') 
sys.path.append('./request')

from userRequest import *

req1 = userRequest()
req1.getUserById(1)

#user1 = User('toto', 'titi', 'tata', 'tutu')
#session.add(user1)
#session.commit()
