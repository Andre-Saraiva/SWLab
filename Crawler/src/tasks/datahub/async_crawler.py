'''
Created on 17/11/2015

@author: Joao Pimentel
'''
import asyncio
import aiohttp

from ..async_utils import wait_with_progress

from ..database.async_connection import engine

from ..database.queries import load_types, first
from ..database.queries import min_created_date, max_modified_date
from ..database.queries import (
    fq_dataset_by_name, fq_insert_feature, fq_datahub_dataset_insert,
    fq_update_feature, fq_select_dataset, fq_update_dataset, fi_resource,
    fq_select_resource, fq_insert_resource, fi_dataset_feature,
    fq_select_dataset_feature, fq_update_dataset_feature,
    fq_insert_dataset_feature)

from .shared import extra_links, relationships, update_done


class AsyncCrawler:

    def __init__(self, loop, count):
        self.todo = set()
        self.done = {}
        self.types_id = load_types()
        self.sem = asyncio.Semaphore(count)
        self.tasks = set()
        self.loop = loop
        self.connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)

    def __del__(self):
        self.connector.close()

    @asyncio.coroutine
    def __call__(self, names):
        """ Executa crawler """
        self.engine = yield from engine()

        for name in names:
            self.todo.add(name)
            self.tasks.add(self.get_page(name))

        yield from wait_with_progress(self.tasks)

    @asyncio.coroutine
    def get_page(self, name):
        """ Carrega página de dataset do datahub """
        with (yield from self.sem):
            self.todo.remove(name)
            url = 'http://datahub.io/api/rest/dataset/{}'.format(name)
            try:
                resp = yield from aiohttp.request('get', url,
                                                  connector=self.connector)
            except Exception as exc:
                print('...', url, 'has error', repr(str(exc)))
                self.done[name] = False
            else:
                if (resp.status == 200 and
                    ('json' in resp.headers.get('content-type'))):
                    data = (yield from resp.json())
                    self.done[name] = yield from self.process_dataset(data, url)
                else:
                    self.done[name] = False
                resp.close()
            update_done(self.done, name)


    @asyncio.coroutine
    def process_dataset(self, data, url):
        """ Processa JSON de dataset do datahub """
        try:
            dataset = yield from self.dataset_by_name(data['name'])
            dataset = yield from self.update_dataset(dataset, data)
            fid = dataset.feature_id

            extras_resource = yield from self.create_resource(
                'datahub/extras', url, 'datahub', 'Extras', True, fid)
            relationships_resource = yield from self.create_resource(
                'datahub/relationships', url, 'datahub', 'Relationships', True, fid)

            for resource in data['resources']:
                yield from self.create_resource(
                    resource['format'], resource['url'], 'datahub',
                    resource['description'], None, dataset.feature_id)

            for name, count in extra_links(data['extras']):
                other = yield from self.dataset_by_name(name)
                yield from self.create_dataset_feature(
                    extras_resource, dataset, other, count)

            for relationship in relationships(data['relationships']):
                other = yield from self.dataset_by_name(relationship['object'])
                yield from self.create_dataset_feature(
                    relationships_resource, dataset, other, relationship['comment'])
            return True
        except Exception as exc:
            print('...', data['name'], 'has error', repr(str(exc)))
            return False

    @asyncio.coroutine
    def dataset_by_name(self, name):
        """ Seleciona dataset por nome do datahub
        Se não existir, cria novo """
        dselect = fq_dataset_by_name(name)
        finsert = fq_insert_feature(self.types_id['dataset'])
        dinsert = fq_datahub_dataset_insert(name)

        with (yield from self.engine) as conn:
            dataset = first((yield from conn.execute(dselect)))
            if dataset:
                return dataset

            feature = first((yield from conn.execute(finsert)))
            return first((yield from conn.execute(
                dinsert.values(feature_id=feature.feature_id))))

    @asyncio.coroutine
    def update_dataset(self, dataset, data):
        """ Atualiza dataset e namespace de feature de acordo com dados """
        namespace = data['url']
        if 'namespace' in data['extras']:
            namespace = data['extras']['namespace']

        fid = dataset.feature_id
        fupdate = fq_update_feature(namespace, fid)
        dselect = fq_select_dataset(fid)
        dupdate = fq_update_dataset(data['url'], data['id'], fid)

        with (yield from self.engine) as conn:
            yield from conn.execute(fupdate)
            ds = first((yield from conn.execute(dselect)))
            created_at = min_created_date(ds, data['metadata_created'])
            modified_at = max_modified_date(ds, data['metadata_modified'])

            return first((yield from conn.execute(dupdate.values(
                created_at=created_at, modified_at=modified_at))))

    @asyncio.coroutine
    def create_resource(self, rformat, url, source, desc, is_online, fid):
        """ Seleciona recurso por url, format e source
        Se recurso não existir, cria novo """
        identifier = fi_resource(rformat, url, source)
        rselect = fq_select_resource(identifier)
        rinsert = fq_insert_resource(identifier, desc, is_online, fid)

        with (yield from self.engine) as conn:
            resource = first((yield from conn.execute(rselect)))
            if resource:
                return resource
            return first((yield from conn.execute(rinsert)))

    @asyncio.coroutine
    def create_dataset_feature(self, resource, dataset, feature, count):
        """ Cria relacionamento entre dataset e feature
        Se existir algum, atualiza o count """
        identifier = fi_dataset_feature(
            dataset.feature_id, feature.feature_id, resource.resource_id)

        dfselect = fq_select_dataset_feature(identifier)
        dfupdate = fq_update_dataset_feature(identifier, count)
        dfinsert = fq_insert_dataset_feature(identifier, count)

        with (yield from self.engine) as conn:
            df = first((yield from conn.execute(dfselect)))
            return first(
                (yield from conn.execute(dfupdate if df else dfinsert)))
