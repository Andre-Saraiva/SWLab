'''
Created on 16/11/2015

@author: Joao Pimentel
'''
import requests

from ..utils import progress

from ..database.connection import connect

from ..database.queries import load_types, first
from ..database.queries import min_created_date, max_modified_date
from ..database.queries import (
    fq_dataset_by_name, fq_insert_feature, fq_datahub_dataset_insert,
    fq_update_feature, fq_select_dataset, fq_update_dataset, fi_resource,
    fq_select_resource, fq_insert_resource, fi_dataset_feature,
    fq_select_dataset_feature, fq_update_dataset_feature,
    fq_insert_dataset_feature)

from .shared import extra_links, relationships, update_done

class SyncCrawler:

    def __init__(self):
        self.todo = set()
        self.done = {}
        self.types_id = load_types()

    def __call__(self, names):
        """ Executa crawler """
        self.engine = connect

        for name in progress(names):
            self.todo.add(name)
            self.get_page(name)

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
                self.done[name] = self.process_dataset(data, url)
            else:
                self.done[name] = False
            resp.close()
        update_done(self.done, name)

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
            return True
        except Exception as exc:
            print('...', data['name'], 'has error', repr(str(exc)))
            return False


    def dataset_by_name(self, name):
        """ Seleciona dataset por nome do datahub
        Se não existir, cria novo """
        dselect = fq_dataset_by_name(name)
        finsert = fq_insert_feature(self.types_id['dataset'])
        dinsert = fq_datahub_dataset_insert(name)

        with self.engine as conn:
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

        fid = dataset.feature_id
        fupdate = fq_update_feature(namespace, fid)
        dselect = fq_select_dataset(fid)
        dupdate = fq_update_dataset(data['url'], data['id'], fid)

        with self.engine as conn:
            conn.execute(fupdate)
            ds = first(conn.execute(dselect))
            created_at = min_created_date(ds, data['metadata_created'])
            modified_at = max_modified_date(ds, data['metadata_modified'])

            return first(conn.execute(dupdate.values(
                created_at=created_at, modified_at=modified_at)))


    def create_resource(self, rformat, url, source, desc, is_online, fid):
        """ Seleciona recurso por url, format e source
        Se recurso não existir, cria novo """
        identifier = fi_resource(rformat, url, source)
        rselect = fq_select_resource(identifier)
        rinsert = fq_insert_resource(identifier, desc, is_online, fid)


        with self.engine as conn:
            resource = first(conn.execute(rselect))
            if resource:
                return resource
            return first(conn.execute(rinsert))

    def create_dataset_feature(self, resource, dataset, feature, count):
        """ Cria relacionamento entre dataset e feature
        Se existir algum, atualiza o count """
        identifier = fi_dataset_feature(
            dataset.feature_id, feature.feature_id, resource.resource_id)

        dfselect = fq_select_dataset_feature(identifier)
        dfupdate = fq_update_dataset_feature(identifier, count)
        dfinsert = fq_insert_dataset_feature(identifier, count)

        with self.engine as conn:
            df = first(conn.execute(dfselect))
            return first(conn.execute(dfupdate if df else dfinsert))
