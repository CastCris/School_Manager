from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

##
def reset(engine:object)->None:
    with open('./database/map/schema.sql', 'r') as file:
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


#
engine = create_engine('mariadb://school:@localhost/schoolDB', echo=True)

reset(engine)

Base = automap_base()
# Base.prepare(engine, reflect=True)
Base.prepare(autoload_with=engine, schema="schoolDB")

print(Base.metadata.tables.keys())

##

Session = sessionmaker()
session = Session()
