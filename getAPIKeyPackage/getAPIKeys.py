from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from getAPIKeyPackage.getAPIKeys_database_setup import Base, APIkeys

app = Flask(__name__)

# absolute path for database used
engine = create_engine('sqlite:////vagrant/myAPIkeys.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

def getAPIKey(provider, app, key):
    appkey = session.query(APIkeys).filter_by(provider=provider, app=app, key=key).one()
    return appkey.value    
    