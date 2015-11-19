'''
Created on 19/11/2015

@author: Joao Pimentel
'''
from urllib.parse import urlparse
from itertools import groupby
from collections import OrderedDict, defaultdict
from sqlalchemy import select, or_, and_
from .models import engine
from .models import features, datasets


class Url:
    def __init__(self, fid, url, source, content_type=None):
        self.fid = fid
        self.url = url
        self.source = source
        self.content_type = content_type

    def __eq__(self, other):
        return (self.url == other.url and
                self.content_type == other.content_type)

    def __hash__(self):
        return hash((self.url, self.content_type))

    def __repr__(self):
        return self.url


def urls_list():
    conn = engine.connect()
    sel1 = select([datasets.c.feature_id, datasets.c.url]).where(
        and_(datasets.c.url is not None, datasets.c.url != ""))
    sel2 = select([features.c.feature_id,
                   features.c.namespace.label('url')]).where(and_(
        features.c.namespace is not None, features.c.namespace != ""))
    sel = sel1.union(sel2)
    result = conn.execute(sel)
    urls = [(row.feature_id, urlparse(row.url.strip()))
            for row in result if row.url.strip()]
    conn.close()
    return urls


def group_domains(urls):
    groups = OrderedDict()
    for domain, urls in groupby(urls, lambda x: x[1].netloc):
        groups[domain] = [url for url in urls]
    return groups


def void_urls(groups):
    voids_groups = OrderedDict()
    for domain, urls in groups.items():
        voids = voids_groups[domain] = set()
        fid = urls[0][0]
        protocol = urls[0][1].scheme

        voids.add(Url(fid, "{}://{}".format(
            protocol, domain), "canonica1", content_type="rdf"))
        voids.add(Url(fid, "{}://{}/void.ttl".format(
            protocol, domain), "canonica2"))
        voids.add(Url(fid, "{}://{}/.well-known/void".format(
            protocol, domain), "canonica3"))

        for url in urls:
            path = [x for x in url[1].path.split('/') if x]
            if not path:
                continue
            if '.ttl' in path[-1]:
                voids.add(Url(url[0], "{}://{}/{}".format(
                    protocol, domain, '/'.join(path)), "canonica4"))
            if '.' in path[-1]: # arquivo, substitui por void
                path = path[:-1]
            if not path:
                continue
            path = '/'.join(path)
            voids.add(Url(url[0], "{}://{}/{}".format(
                protocol, domain, path), "canonica1", content_type="rdf"))
            voids.add(Url(url[0], "{}://{}/{}/void.ttl".format(
                protocol, domain, path), "canonica2"))
            voids.add(Url(url[0], "{}://{}/{}/.well-known/void".format(
                protocol, domain, path), "canonica3"))
    return voids_groups


def void_list():
    return void_urls(group_domains(urls_list()))