from pydantic import EmailStr

from database import Base, sessionlocal , engine
from sqlalchemy import Column, Integer, String , ForeignKey

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)

    is_admin = Column(Integer, default=0)  

class Order(Base):
    __tablename__ = "orders"
    
    email = Column(String, ForeignKey("users.email"), primary_key=True)
    item = Column(String)
    quantity = Column(Integer)

class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, unique=True, index=True)
    quantity = Column(Integer)

Base.metadata.create_all(bind=engine)