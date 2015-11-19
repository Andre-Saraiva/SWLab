'''
Created on 19/11/2015

@author: Joao Pimentel
'''
import requests
import tqdm
from collections import defaultdict
from .models import engine, check_voids


class VoidCrawler:
    def __init__(self):
        self.done = defaultdict(dict)

    def __enter__(self):
        self.conn = engine.connect()
        return self.conn

    def __exit__(self, *args):
        self.conn.close()

    def iterator(self, groups):
        for group, urls in groups.items():
            for url in urls:
                yield group, url

    def __call__(self, groups):
        count = sum(len(x) for x in groups.values())
        for group, url in tqdm.tqdm(self.iterator(groups), total=count):
            self.get_url(group, url)

    def get_url(self, group, url):
        try:
            headers = None
            if url.content_type == 'rdf':
                headers = {'content-type': 'text/turtle'}
            resp = requests.get(url.url, headers=headers)
        except Exception as exc:
            self.done[group][url] = False
        else:
            if resp.status_code == 200:
                self.done[group][url] = True
                self.process(group, url, resp)
            else:
                self.done[group][url] = False
            resp.close()

    def process(self, group, url, resp):
        cvinsert = check_voids.insert().values(
            content_type=resp.headers.get('content-type'),
            url=url.url,
            source=url.source,
            feature_id=url.fid,
            content=resp.content)
        with self as conn:
            conn.execute(cvinsert)

