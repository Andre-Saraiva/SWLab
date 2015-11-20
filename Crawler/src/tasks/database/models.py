'''
Created on 16/11/2015

@author: Joao Pimentel
'''
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, DateTime, Boolean, LargeBinary
from sqlalchemy import ForeignKeyConstraint

from .connection import metadata, connect


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
    ForeignKeyConstraint(['feature_id'], [features.c.feature_id],
                         name='fk_resources_features',
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

check_voids = Table(
    'check_voids', metadata,
    Column('check_void_id', Integer, primary_key=True),
    Column('content_type', String(255)),
    Column('url', String(2083)),
    Column('source', String(45)),
    Column('feature_id', Integer),
    Column('content', LargeBinary),
    Column('encoding', String(255)),
    Column('hash', String(255)),
    ForeignKeyConstraint(['feature_id'], [features.c.feature_id],
                         name='fk_check_voids_features',
                         ondelete='NO ACTION', onupdate='NO ACTION')

)

resource_cache = Table(
    'resource_cache', metadata,
    Column('resource_id', Integer, primary_key=True),
    Column('hash', String(255)),
    Column('content', LargeBinary),
    Column('content_type', String(255)),
    Column('encoding', String(255)),
    ForeignKeyConstraint(['resource_id'], [resources.c.resource_id],
                         name='fk_resource_cache_resources',
                         ondelete='NO ACTION', onupdate='NO ACTION')
)


def create_schema():
    """ Cria tabelas e popula tipos de features """
    if resource_cache.exists():
        resource_cache.drop()
    if check_voids.exists():
        check_voids.drop()
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
    check_voids.create()
    resource_cache.create()

    with connect as conn:
        conn.execute(
            types.insert(), [
                {'name': 'dataset'},
                {'name': 'property'},
                {'name': 'class'},
                {'name': 'vocabulary'},
            ])
