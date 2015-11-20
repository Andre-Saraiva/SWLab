'''
Created on 19/11/2015

@author: Joao Pimentel
'''
import asyncio
import aiohttp

from collections import defaultdict

from ..async_utils import wait_with_progress

from ..database.async_connection import engine

from ..database.queries import first
from ..database.queries import fq_insert_check_void, fq_select_check_void


class AsyncVoidCrawler:

    def __init__(self, loop, count):
        self.done = defaultdict(dict)
        self.sem = defaultdict(lambda: asyncio.Semaphore(count))
        self.connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)
        self.tasks = set()
        self.loop = loop

    def iterator(self, groups):
        for group, urls in groups.items():
            for url in urls:
                yield group, url

    @asyncio.coroutine
    def __call__(self, groups):
        self.engine = yield from engine()

        for group, url in self.iterator(groups):
            self.tasks.add(self.get_url(group, url))

        yield from wait_with_progress(self.tasks)

    def __del__(self):
        self.connector.close()

    @asyncio.coroutine
    def get_url(self, group, url):
        cvselect = fq_select_check_void(url.url)
        with (yield from self.engine) as conn:
            check_void = first((yield from conn.execute(cvselect)))
            if check_void:
                return
        with (yield from self.sem[group]):
            _url = url.url
            history = {_url}
            for _ in range(10):
                try:
                    headers = None
                    if url.content_type == 'rdf':
                        headers = {'content-type': 'text/turtle'}
                    resp = yield from aiohttp.request('get', _url,
                                                      connector=self.connector,
                                                      headers=headers)
                except Exception:
                    self.done[group][url] = False
                else:
                    if resp.status == 200:
                        self.done[group][url] = True
                        yield from self.process(
                            group, url.fid, _url, url.source,
                            (yield from resp.read()),
                            resp.headers.get('content-type'),
                            resp.headers.get('Content-Encoding'))
                    elif resp.status in (300, 301, 302, 303, 307):
                        location = resp.headers.get('location')
                        if location and not location in history:
                            print('REDIRECT', _url, '->', location)
                            _url = location
                            history.add(_url)
                            resp.close()
                            continue
                    else:
                        self.done[group][url] = False
                    resp.close()
                break

    @asyncio.coroutine
    def process(self, group, fid, url, source, content, content_type, encoding):
        cvinsert = fq_insert_check_void(fid, url, source, content,
                                        content_type, encoding)

        with (yield from self.engine) as conn:
            yield from conn.execute(cvinsert)
