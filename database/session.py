from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from begin.globals import Message

from .methods.crypt import *

import re

##
def mariadb_database_drop(engine:object)->None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    metadata.drop_all(engine)

def mariadb_database_create(engine:object)->object:
    with open('database/casts/schema.sql', 'r') as file:
        sql = file.read()

    with engine.connect() as connection:
        connection.execute(text(sql))
        connection.commit()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    Base = declarative_base(metadata=metadata)
    return Base

def mariadb_init()->None:
    global engine

    global Base
    global session

    #
    engine = create_engine('mariadb://school:@localhost/schoolDB', echo=True)

    mariadb_database_drop(engine)
    Base = mariadb_database_create(engine)

    Session = sessionmaker(bind=engine)
    session = Session()


engine = Base = session = None

mariadb_init()
