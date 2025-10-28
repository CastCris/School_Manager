from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from begin.globals import Message

import re

##
def reset(engine:object)->None:
    with open('./database/casts/schema.sql', 'r') as file:
        sql = text(file.read())

    with engine.connect() as connection:
        inspector = inspect(connection)
        for i in inspector.get_table_names():
            foreignKeys_dependded_command = f" \
                SELECT CONCAT('ALTER TABLE ', TABLE_NAME, ' DROP FOREIGN KEY ', CONSTRAINT_NAME, ';') \
                FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE \
                WHERE REFERENCED_TABLE_NAME = '{i}' \
                AND TABLE_SCHEMA = 'schoolDB'; \
                "

            foreignKeys_dependded = connection.execute(text(foreignKeys_dependded_command))
            statements = [ list(dict(j).values())[0] for j in foreignKeys_dependded.mappings().all() ]

            # Delete all foregin keys dependences
            for j in statements:
                connection.execute(text(j))

            connection.execute(text(f"DROP TABLE IF EXISTS {i};"))
            connection.commit()

        connection.execute(sql)

    file.close()


##
engine = create_engine('mariadb://school:@localhost/schoolDB', echo=True)

metadata = MetaData()
metadata.reflect(bind=engine)

Base = declarative_base(metadata=metadata)

Session = sessionmaker()
session = Session()

FIELD_CIPHER = lambda model: [ i for i in model.__dict__.keys() if re.search("^cipher_*.", i)]
FIELD_HASHED = lambda model: [ i for i in model.__dict__.keys() if re.search("^hashed_*.", i)]

##
op_comps = {
    'lt': lambda column, value: column < value,
    'lte': lambda column, value: column <= value,

    'gt': lambda column, value: column > value,
    'gte': lambda column, value: column >= value,

    'eq': lambda column, value: column == value,
    'ne': lambda column, calue: column != value
}

def session_insert(model:object, **kwargs)->object|None:
    try:
        field_cipher = getattr(model, "FIELD_CIPHER", [])
        field_hasehd = getattr(model, "FIELD_HASEHD", [])

        kwargs_miss = {}
        if not "dek" in kwargs.keys() and "dek" in model.__dict__.keys():
            kwargs_miss["dek"] = key_crypt(AESGCM.generate_key(bit_length=256))

        for i in field_cipher:
            dek = key_decrypt(kwargs["dek"])
            attr_name = i.split('cipher_')[0]

            if not attr_name in kwargs.keys():
                continue

            kwargs_miss[f"cipher_{attr_name}"] = clm_encrypt(kwargs[attr_name], dek)

        for i in field_hashed:
            dek = key_decrypt(kwargs["dek"])
            attr_name = i.split('hashed_')[0]

            if not attr_name in kwargs.keys():
                continue

            kwargs_miss[f"hashed_{attr_name}"] = clm_encrypt(kwargs[attr_name], dek)

        ##
        instance = model(**kwargs, **kwargs_miss)
        session.add(instance)

        return instance
    
    except Exception as e:
        Message.error('session_insert', e)
        session.rollback()

        return None

def session_delete(instances:tuple)->None:
    try:
        for i in instances:
            session.delete(i)

        session.commit()

    except Exception as e:
        Message.error('session_delete', e)
        session.rollback()

def session_update(instances:tuple, **kwargs)->None:
    try:
        for i in instances:
            model_update(i, **kwargs)

    except Exception as e:
        Message.error('session_update', e)
        session.rollback()

def session_get(model:object, **kwargs)->tuple|None:
    try:
        filters = []

        for i in kwargs.keys():
            column_name, op_name = i, 'eq'

            if '__' in i:
                column_name, op_name = i.split('__')

            op = op_cmp[op_name]
            column = getattr(model, column_name, None)

            filters.append(op(column, kwargs[i]))

        query = session.query(model).filter(*filters).all()
        return query

    except Exception as e:
        Message.error('session_get', e)
        session.rollback()

        return None


def model_update(instance:object, **kwargs)->None:
    from begin.globals import Token

    ##
    try:
        model = type(instance, (instance.__class__, ), {})

        field_cipher = getattr(model, "FIELD_CIPHER", [])
        field_hashed = getattr(model, "FIELD_HASHED", [])

        kwargs_copy = kwargs.copy()

        for i in kwargs.values():
            dek_cryptted = getattr(instance, "dek", None)
            if dek_cryptted is None:
                continue

            dek = key_decrypt(instance.dek)

            if i in field_cipher:
                kwargs_copy[i] = clm_encrypt(kwargs[i], dek)

            elif i in field_hashed:
                kwargs_copy[i] = Token.crypt_sha256(kwargs[i])

        for i in kwargs_copy.values():
            setattr(instance, i, kwargs_copy[i])

        session.commit()

    except Exception as e:
        Message.error('model_update', e)
        session.rollback()
