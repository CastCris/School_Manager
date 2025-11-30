import sqlalchemy
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from begin.globals import Messages

from .methods.crypt import *

import re
import time

##
def mariadb_database_drop(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)

def mariadb_database_create(engine:object)->object:
    with open('database/casts/mariadb_schema.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def mariadb_init()->None:
    import os

    ##
    global engine

    global Base
    global session

    #
    MARIADB_HOST = os.getenv('MYSQL_HOST', 'mariadb')
    MARIADB_USER = os.getenv('MYSQL_USER', 'school')
    MARIADB_PASSWORD = os.getenv('MYSQL_PASSWORD', 'admin')
    MARIADB_DATABASE = os.getenv('MYSQL_DATABASE', 'schoolDB')

    url = f"mariadb://{MARIADB_USER}:{MARIADB_PASSWORD}@{MARIADB_HOST}/{MARIADB_DATABASE}"
    print(url)

    engine = create_engine(url, echo=True)

    mariadb_database_drop(engine)
    Base = mariadb_database_create(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


def sqlite_database_drop(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)

def sqlite_database_create(engine:object)->object:
    with open('database/casts/sqlite_schema.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        for i in sql.split(';'):
            connection.execute(text(i))

        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def sqlite_init()->None:
    global engine
    global metadata

    global Base
    global session

    #
    engine = create_engine('sqlite:///schoolDB', echo=True)

    sqlite_database_drop(engine)
    Base = sqlite_database_create(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()
    metadata.reflect(bind=engine)

##
engine = metadata = Base = session = None

# mariadb_init()

for _ in range(10):
    try:
        mariadb_init()

    except sqlalchemy.exec.OperationError:
        print('Try connect to database again')
        time.sleep(2)
    # sqlite_init()
