'''
Created on 16/11/2015

@author: Joao Pimentel
'''
from datetime import datetime
from sqlalchemy import create_engine, Table, MetaData, Column
from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy import ForeignKeyConstraint, select, and_


USER = "postgres"
PASSWORD = "postgres"
HOST = "127.0.0.1"
DATABASE = "swlab"


engine = create_engine(
    "postgresql+psycopg2://{}:{}@{}/{}".format(USER, PASSWORD, HOST, DATABASE),
    client_encoding="utf8")

metadata = MetaData()
metadata.bind = engine


types = Table(
    'types', metadata,
    Column('type_id', Integer, primary_key=True),
    Column('name', String(45))
)


features = Table(
    'features', metadata,
    Column('feature_id', Integer, primary_key=True),
    Column('namespace', String(2083)),
    Column('type_id', Integer, nullable=False),
    ForeignKeyConstraint(['type_id'], [types.c.type_id],
                         name='fk_features_types',
                         ondelete='NO ACTION', onupdate='NO ACTION')
)


datasets = Table(
    'datasets', metadata,
    Column('feature_id', Integer, primary_key=True),
    Column('meta', String(45)),
    Column('meta_id', String(45)),
    Column('meta_url', String(2083)),
    Column('name', String(150)),
    Column('url', String(2083)),
    Column('created_at', DateTime),
    Column('modified_at', DateTime),
    ForeignKeyConstraint(['feature_id'], [features.c.feature_id], 
                         name='fk_datasets_features',
                         ondelete='NO ACTION', onupdate='NO ACTION')
)


resources = Table(
    'resources', metadata,
    Column('resource_id', Integer, primary_key=True),
    Column('format', String(500)),
    Column('url', String(10000)),
    Column('source', String(45)),
    Column('description', String(5000)),
    Column('is_online', Boolean),
    Column('feature_id', Integer),
    ForeignKeyConstraint(['feature_id'], [datasets.c.feature_id], 
                         name='fk_resources_datasets',
                         ondelete='NO ACTION', onupdate='NO ACTION')
)


dataset_features = Table(
    'dataset_features', metadata,
    Column('ds_feature_id', Integer, primary_key=True),
    Column('ft_feature_id', Integer, primary_key=True),
    Column('count', Integer),
    Column('resource_id', Integer, primary_key=True),
    ForeignKeyConstraint(['ds_feature_id'], [datasets.c.feature_id],
                         name='fk_dataset_features_datasets',
                         ondelete='NO ACTION', onupdate='NO ACTION'),
    ForeignKeyConstraint(['ft_feature_id'], [features.c.feature_id],
                         name='fk_dataset_features_features',
                         ondelete='NO ACTION', onupdate='NO ACTION'),
    ForeignKeyConstraint(['resource_id'], [resources.c.resource_id],
                         name='fk_dataset_features_resources',
                         ondelete='NO ACTION', onupdate='NO ACTION')
)


def activate_logging():
    """ Ativa log do SQLAlchemy """
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def create_database():
    """ Cria database """
    eng = create_engine(
        "postgres://{}:{}@{}/postgres".format(USER, PASSWORD, HOST),
        client_encoding="utf8")
    
    conn = engine.connect()
    conn.execute('commit')
    conn.execute('create database {}'.format(DATABASE))
    conn.close()


def create_schema():
    """ Cria tabelas e popula tipos de features """
    if dataset_features.exists():
        dataset_features.drop()
    if resources.exists():
        resources.drop()
    if datasets.exists():
        datasets.drop()
    if features.exists():
        features.drop()
    if types.exists():
        types.drop()
    types.create()
    features.create()
    datasets.create()
    resources.create()
    dataset_features.create()
    
    conn = engine.connect()
    conn.execute(
        types.insert(), [
            {'name': 'dataset'},
            {'name': 'property'},
            {'name': 'class'},
            {'name': 'vocabulary'},
        ])
    conn.close()


def load_types():
    """ Lê tipos de features e retorna dicionário """
    conn = engine.connect()
    result = conn.execute(select([types]))
    types_id = {name: tid for tid, name in result.fetchall()}
    conn.close()
    return types_id


def to_where(table, identifier):
    """ Transforma dicionário em condição de where """
    return and_((getattr(table.c, name) == value) 
                for name, value in identifier.items())
    

def to_date(x):
    if isinstance(x, str):
        format = '%Y-%m-%dT%H:%M:%S'
        if '.' in x:
            format += '.%f'
        return datetime.strptime(x, format)
    return x

def to_int(x):
    if isinstance(x, int):
        return x
    if x.startswith('>'):
        x = x[1:]
    if '.' in x:
        x = x.replace('.', '')
    x = x.strip()
    if x.isdigit():
        return x
    return None
    

def first(gen):
    """ Retorna primeiro elemento """
    for x in gen:
        return x
