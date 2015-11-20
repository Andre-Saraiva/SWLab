'''
Created on 19/11/2015

@author: Joao Pimentel
'''
import requests

from collections import defaultdict

from ..utils import progress

from ..database.connection import connect

from ..database.queries import first
from ..database.queries import fq_insert_check_void, fq_select_check_void


class VoidCrawler:
    def __init__(self):
        self.done = defaultdict(dict)

    def iterator(self, groups):
        for group, urls in groups.items():
            for url in urls:
                yield group, url

    def __call__(self, groups):
        self.engine = connect

        count = sum(len(x) for x in groups.values())
        for group, url in progress(self.iterator(groups), total=count):
            self.get_url(group, url)

    def get_url(self, group, url):
        cvselect = fq_select_check_void(url.url)
        with self.engine as conn:
            check_void = first(conn.execute(cvselect))
            if check_void:
                return

        _url = url.url
        history = {_url}
        for _ in range(10):
            try:
                headers = None
                if url.content_type == 'rdf':
                    headers = {'content-type': 'text/turtle'}
                resp = requests.get(_url, headers=headers)
            except Exception:
                self.done[group][url] = False
            else:
                if resp.status_code == 200:
                    self.done[group][url] = True
                    self.process(
                        group, url.fid, _url, url.source, resp.content,
                        resp.headers.get('content-type'), resp.encoding)
                elif resp.status_code in (300, 301, 302, 303, 307):
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

    def process(self, group, fid, url, source, content, content_type, encoding):
        cvinsert = fq_insert_check_void(fid, url, source, content,
                                        content_type, encoding)

        with self.engine as conn:
            conn.execute(cvinsert)
