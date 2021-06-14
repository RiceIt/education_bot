import os


class Configuration:
    DEV = False
    POSTGRESQL_USER = os.environ["POSTGRESQL_USER"]
    POSTGRESQL_PASSWORD = os.environ["POSTGRESQL_PASSWORD"]
    POSTGRESQL_DBNAME = 'education'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@localhost/{POSTGRESQL_DBNAME}'
