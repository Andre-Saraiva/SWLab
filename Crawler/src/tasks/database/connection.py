'''
Created on 20/11/2015

@author: Joao Pimentel
'''
from sqlalchemy import create_engine, MetaData


USER = "postgres"
PASSWORD = "postgres"
HOST = "127.0.0.1"
DATABASE = "swlab"


engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE),
    client_encoding="utf8")


metadata = MetaData()
metadata.bind = engine


class Connection:
    def __enter__(self):
        self.conn = engine.connect()
        return self.conn

    def __exit__(self, *args):
        self.conn.close()


connect = Connection()


def create_database():
    """ Cria database """
    eng = create_engine(
        "postgres://{}:{}@{}/postgres".format(USER, PASSWORD, HOST),
        client_encoding="utf8")

    conn = eng.connect()
    conn.execute('commit')
    conn.execute('create database {}'.format(DATABASE))
    conn.close()


def activate_logging():
    """ Ativa log do SQLAlchemy """
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
