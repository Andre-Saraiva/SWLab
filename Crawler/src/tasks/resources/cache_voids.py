'''
Created on 20/11/2015

@author: Joao Pimentel
'''

import requests

from ..utils import progress

from ..database.connection import connect

from ..database.queries import first
from ..database.queries import q_select_void, q_update_void
from ..database.queries import fq_select_resource_cache
from ..database.queries import fq_insert_resource_cache


def void_resources():
    with connect as conn:
        return list(conn.execute(q_select_void))


def update_description():
    with connect as conn:
        conn.execute(q_update_void)


def crawler(resources):
    for resource in progress(resources):
        try:
            resp = requests.get(resource.url)
        except:
            pass
        else:
            if (resp.status_code == 200):
                content = resp.content
                content_type = resp.headers.get('content-type')
                encoding = resp.encoding

                rid = resource.resource_id
                rcselect = fq_select_resource_cache(rid)
                rcinsert = fq_insert_resource_cache(
                        rid, content, content_type, encoding)

                with connect as conn:
                    if not first(conn.execute(rcselect)):
                        conn.execute(rcinsert)
            resp.close()
