import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    username = Column(String,unique=True, nullable=False)
    email = Column(String,unique=True,index=True, nullable=False)
    password = Column(String, nullable=False)
    isActive = Column(Boolean, default=True)
    confirmed = Column(Boolean, default=False)

class permissions(str,enum.Enum):
    one = 1
    two = 2

class Profiles(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True)
    id_project = Column(Integer)
    user_type = Column(String)
    permissions = Column('value', Enum(permissions))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User")




