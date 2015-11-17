'''
Created on 16/11/2015

@author: Joao Pimentel
'''
import requests
import tqdm
from datetime import datetime as dt
from sqlalchemy import select
from .models import engine, load_types, first, to_date, to_where
from .models import datasets, features, dataset_features, resources


def extra_links(extras):
    for key, value in extras.items():
        if key.startswith('links:'):
            yield (key[6:], value)



def relationships(relations):
    for relationship in relations:
        if relationship['type'] == 'links_to':
            yield relationship


class SyncCrawler:

    def __init__(self):
        self.todo = set()
        self.done = {}
        self.types_id = load_types()

    def __call__(self, names):
        """ Executa crawler """
        for name in tqdm.tqdm(names):
            self.todo.add(name)
            self.get_page(name)

    def __enter__(self):
        self.conn = engine.connect()
        return self.conn

    def __exit__(self, *args):
        self.conn.close()

    def get_page(self, name):
        """ Carrega página de dataset do datahub """
        self.todo.remove(name)
        url = 'http://datahub.io/api/rest/dataset/{}'.format(name)
        try:
            resp = requests.get(url)
        except Exception as exc:
            print('...', url, 'has error', repr(str(exc)))
            self.done[name] = False
        else:
            if (resp.status_code == 200 and
                ('json' in resp.headers.get('content-type'))):
                data = resp.json()
                self.process_dataset(data, url)
                self.done[name] = True
            else:
                self.done[name] = False
            resp.close()

    def process_dataset(self, data, url):
        """ Processa JSON de dataset do datahub """
        try:
            dataset = self.dataset_by_name(data['name'])
            dataset = self.update_dataset(dataset, data)
            fid = dataset.feature_id
    
            extras_resource = self.create_resource(
                'datahub/extras', url, 'datahub', 'Extras', True, fid)
            relationships_resource = self.create_resource(
                'datahub/relationships', url, 'datahub', 'Relationships', True, fid)
    
            for resource in data['resources']:
                self.create_resource(
                    resource['format'], resource['url'], 'datahub',
                    resource['description'], None, dataset.feature_id)
    
            for name, count in extra_links(data['extras']):
                other = self.dataset_by_name(name)
                self.create_dataset_feature(extras_resource, dataset, other, count)
    
            for relationship in relationships(data['relationships']):
                other = self.dataset_by_name(relationship['object'])
                self.create_dataset_feature(relationships_resource, dataset, other,
                                            relationship['comment'])
        except Exception as exc:
            print('...', data['name'], 'has error', repr(str(exc)))


    def dataset_by_name(self, name):
        """ Seleciona dataset por nome do datahub
        Se não existir, cria novo """
        datahub = 'http://datahub.io/dataset/{}'.format(name)
        dselect = select([datasets]).where(datasets.c.name == name)
        finsert = features.insert().values(
            type_id=self.types_id['dataset']).returning(features)
        dinsert = datasets.insert().values(
            meta='datahub', meta_url=datahub, name=name).returning(datasets)

        with self as conn:
            dataset = first(conn.execute(dselect))
            if dataset:
                return dataset

            feature = first(conn.execute(finsert))
            return first(conn.execute(
                dinsert.values(feature_id=feature.feature_id)))


    def update_dataset(self, dataset, data):
        """ Atualiza dataset e namespace de feature de acordo com dados """
        namespace = data['url']
        if 'namespace' in data['extras']:
            namespace = data['extras']['namespace']

        where = (features.c.feature_id == dataset.feature_id)
        fupdate = features.update().values(namespace=namespace).where(where)
        dselect = select([datasets]).where(where)
        dupdate = datasets.update().values(
            url=data['url'], meta_id=data['id']).where(
                where).returning(datasets)

        with self as conn:
            conn.execute(fupdate)
            ds = first(conn.execute(dselect))
            created_at = min(
                to_date(ds.created_at) if ds and ds.created_at else dt.max,
                to_date(data['metadata_created']))
            modified_at = max(
                to_date(ds.modified_at) if ds and ds.modified_at else dt.min,
                to_date(data['metadata_modified']))

            return first(conn.execute(dupdate.values(
                created_at=created_at, modified_at=modified_at)))


    def create_resource(self, format, url, source, description, is_online, fid):
        """ Seleciona recurso por url, format e source
        Se recurso não existir, cria novo """
        identifier = dict(format=format, url=url, source=source)
        rselect = select([resources]).where(to_where(resources, identifier))
        rinsert = resources.insert().values(
            description=description, is_online=is_online, feature_id=fid,
            **identifier).returning(resources)

        with self as conn:
            resource = first(conn.execute(rselect))
            if resource:
                return resource
            return first(conn.execute(rinsert))

    def create_dataset_feature(self, resource, dataset, feature, count):
        """ Cria relacionamento entre dataset e feature
        Se existir algum, atualiza o count """
        identifier = dict(ds_feature_id=dataset.feature_id,
                          ft_feature_id=feature.feature_id,
                          resource_id=resource.resource_id)
        where = to_where(dataset_features, identifier)
        dfselect = select([dataset_features]).where(where)
        dfupdate = dataset_features.update().values(count=count).where(
            where).returning(dataset_features)
        dfinsert = dataset_features.insert().values(
            count=count, **identifier).returning(dataset_features)

        with self as conn:
            df = first(conn.execute(dfselect))
            return first(conn.execute(dfupdate if df else dfinsert))
        

