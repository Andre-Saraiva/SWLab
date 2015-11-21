'''
Created on 20/11/2015

@author: Joao Pimentel
'''
import chardet
from datetime import datetime as dt
from hashlib import sha1
from sqlalchemy import select, and_, or_
from .models import check_voids, datasets, dataset_features, features, types
from .models import resources, resource_cache
from .connection import connect


def to_where(table, identifier):
    """ Transforma dicionário em condição de where """
    return and_((getattr(table.c, name) == value)
                for name, value in identifier.items())


def to_int(x):
    if isinstance(x, int):
        return x
    if x.startswith('>'):
        x = x[1:]
    if '.' in x:
        x = x.replace('.', '')
    x = x.strip()
    if x.isdigit():
        return x
    return None


def to_date(x):
    if isinstance(x, str):
        format = '%Y-%m-%dT%H:%M:%S'
        if '.' in x:
            format += '.%f'
        return dt.strptime(x, format)
    return x


def load_types():
    """ Lê tipos de features e retorna dicionário """
    with connect as conn:
        result = conn.execute(select([types]))
        types_id = {name: tid for tid, name in result.fetchall()}
    return types_id


def first(gen):
    """ Retorna primeiro elemento """
    for x in gen:
        return x


def min_created_date(ds, created):
    return min(
        to_date(ds.created_at) if ds and ds.created_at else dt.max,
        to_date(created))


def max_modified_date(ds, modified):
    return max(
        to_date(ds.modified_at) if ds and ds.modified_at else dt.min,
        to_date(modified))


def update_encoding(encoding, content):
    if not encoding:
        try:
            encoding = chardet.detect(bytes(content))['encoding']
        except Exception as exc:
            print(exc)
    return encoding


q_delete_empty_check_voids = check_voids.delete().where(
    check_voids.c.content == b"")


fq_select_check_void = lambda url: select([check_voids]).where(
    check_voids.c.url == url)


def fq_insert_check_void(fid, url, source, content, content_type, encoding):
    encoding = update_encoding(encoding, content)
    return check_voids.insert().values(
        feature_id=fid, url=url, source=source, content=content,
        content_type=content_type, encoding=encoding,
        hash=sha1(content).hexdigest())

fq_dataset_by_name = lambda name: select([datasets]).where(
    datasets.c.name == name)


fq_insert_feature = lambda tid: features.insert().values(
    type_id=tid).returning(features)


fq_datahub_dataset_insert = lambda name: datasets.insert().values(
    meta='datahub', meta_url='http://datahub.io/dataset/{}'.format(name),
    name=name).returning(datasets)


fq_update_feature = lambda namespace, fid: features.update().values(
    namespace=namespace).where(features.c.feature_id == fid)


fq_select_dataset = lambda fid: select([datasets]).where(
    datasets.c.feature_id == fid)


fq_update_dataset = lambda url, mid, fid: datasets.update().values(
    url=url, meta_id=mid).where(
        datasets.c.feature_id == fid).returning(datasets)


fi_resource = lambda format, url, source: dict(
    format=format, url=url[:10000], source=source)


fq_select_resource = lambda identifier: select([resources]).where(
    to_where(resources, identifier))


fq_insert_resource = lambda ident, desc, on, fid: resources.insert().values(
    description=desc[:5000], is_online=on, feature_id=fid, **ident).returning(
    resources)


fi_dataset_feature = lambda did, fid, rid: dict(
    ds_feature_id=did, ft_feature_id=fid, resource_id=rid)


fq_select_dataset_feature = lambda ident: select([dataset_features]).where(
    to_where(dataset_features, ident))


fq_update_dataset_feature = lambda ident, count: dataset_features.update(
    ).values(count=to_int(count)).where(
    to_where(dataset_features, ident)).returning(dataset_features)


fq_insert_dataset_feature = lambda ident, count: dataset_features.insert(
    ).values(count=to_int(count), **ident).returning(dataset_features)


q_datasets_url = select([datasets.c.feature_id, datasets.c.url]).where(
    and_(datasets.c.url is not None, datasets.c.url != ""))


q_features_url = select(
    [features.c.feature_id, features.c.namespace.label('url')]).where(
    and_(features.c.namespace is not None, features.c.namespace != ""))


q_urls = q_datasets_url.union(q_features_url)


where_void = or_(
    and_(
        or_(resources.c.format.like("%rdf%"),
            resources.c.format.like("%n3%"),
            resources.c.format.like("%octet-stream%"),
            resources.c.format.like("%turtle%")),
        resources.c.url.like("%void%"),
    ),
    resources.c.format.like("%void%"),
    resources.c.description == "WS(VOID)"
)


q_select_void = select([resources]).where(where_void)


q_update_void = resources.update().values(description="WS(VOID)").where(
    where_void).returning(resources)


fq_update_online_void = lambda rid, online: resources.update().values(
    is_online=online).where(resources.c.resource_id == rid)


fq_select_resource_cache = lambda rid: select([resource_cache]).where(
    resource_cache.c.resource_id == rid)


def fq_insert_resource_cache(rid, content, content_type, encoding):
    encoding = update_encoding(encoding, content)
    return resource_cache.insert().values(
        resource_id=rid,
        hash=sha1(content).hexdigest(),
        content=content,
        content_type=content_type,
        encoding=encoding)
