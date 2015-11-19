'''
Created on 19/11/2015

@author: Joao Pimentel
'''
import asyncio
import aiohttp
import tqdm
from aiopg.sa import create_engine
from collections import defaultdict
from .models import USER, DATABASE, HOST, PASSWORD, check_voids


@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


class AsyncVoidCrawler:

    def __init__(self, loop, count):
        self.done = defaultdict(dict)
        self.sem = asyncio.Semaphore(count)
        self.connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
        self.tasks = set()

    def iterator(self, groups):
        for group, urls in groups.items():
            for url in urls:
                yield group, url

    @asyncio.coroutine
    def __call__(self, groups):
        self.engine = yield from create_engine(
            user=USER, database=DATABASE, host=HOST, password=PASSWORD)
        count = sum(len(x) for x in groups.values())
        for group, url in self.iterator(groups):
            self.tasks.add(self.get_url(group, url))

        yield from wait_with_progress(self.tasks)

    def __del__(self):
        self.connector.close()

    @asyncio.coroutine
    def get_url(self, group, url):
        with (yield from self.sem):
            try:
                headers = None
                if url.content_type == 'rdf':
                    headers = {'content-type': 'text/turtle'}
                resp = yield from aiohttp.request('get', url.url,
                                                  connector=self.connector,
                                                  headers=headers)
            except Exception as exc:
                self.done[group][url] = False
            else:
                if resp.status == 200:
                    self.done[group][url] = True
                    yield from self.process(group, url, resp)
                else:
                    self.done[group][url] = False
                resp.close()

    @asyncio.coroutine
    def process(self, group, url, resp):
        cvinsert = check_voids.insert().values(
            content_type=resp.headers.get('content-type'),
            url=url.url,
            source=url.source,
            feature_id=url.fid,
            content=(yield from resp.read()))
        with (yield from self.engine) as conn:
            yield from conn.execute(cvinsert)

