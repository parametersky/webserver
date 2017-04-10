import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# to use sqlalchemy there are 3 steps:

# first create engine:
engine = create_engine("sqlite:///test.db",echo=True)

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    name=Column(String(80))
Base.metadata.create_all(engine)
# set metadata.bind when Base is in another module
#Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
user = User(name="Kyle")
session.add(user)
session.commit()

items = session.query(User).all()
for item in items:
    print item.name