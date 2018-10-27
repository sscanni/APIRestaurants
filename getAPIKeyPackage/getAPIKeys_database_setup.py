import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

Base = declarative_base()

class APIkeys(Base):

    __tablename__ = 'APIkeys'

    provider= Column(String(250), primary_key=True)
    app= Column(String(250), primary_key=True)
    key = Column(String(250), primary_key=True)
    value = Column(String(250), nullable=False)

#####insert at the end of file######
engine = create_engine('sqlite:////vagrant/myAPIkeys.db?check_same_thread=False')
Base.metadata.create_all(engine)
