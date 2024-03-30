from sqlalchemy import ForeignKey, Text, Column, Integer, String, Sequence
from sqlalchemy.orm import  declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)

    #Base
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)

    items = relationship("Item", back_populates="user", cascade="all, delete, delete-orphan")



class Item(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    #Base
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    website = Column(String)
    notes = Column(Text)

    user = relationship('User', back_populates='items')