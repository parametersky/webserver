from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    name = Column(String(32),nullable=False)
    hash_pw = Column(String(300),nullable=False)
    @property
    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'hash_pw':self.hash_pw
        }
engine = create_engine('sqlite:///users.db')
Base.metadata.create_all(engine)