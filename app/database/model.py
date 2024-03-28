from sqlalchemy import ForeignKey, Text, Column, Integer, String, Sequence
from sqlalchemy.orm import  declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    passwords = relationship("Password", back_populates="user", cascade="all, delete, delete-orphan")



class Password(Base):
    __tablename__ = 'passwords'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    website = Column(String)
    notes = Column(Text)

    user = relationship('User', back_populates='passwords')