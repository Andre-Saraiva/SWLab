'''
Created on 03/11/2015

@author: Luiz Leme
'''

import argparse
import json
from .load_list import load_datahub_list
from .void_url import void_list
from functools import partial

def limit(names, first, last):
    last = last if last != -1 else len(names)
    if last < first:
        first = first - 1 if first else None
        last = last - 1
        names = names[last:first:-1]
    else:
        names = names[first:last]
    return names

def datahub_func(args):
    names = load_datahub_list(args.cache)
    names = limit(names, args.first, args.last)

    if args.async > 0:
        import asyncio
        from .async_crawler import AsyncCrawler
        loop = asyncio.get_event_loop()
        crawler = AsyncCrawler(loop, args.async)
        loop.run_until_complete(crawler(names))
    else:
        from .sync_crawler import SyncCrawler
        crawler = SyncCrawler()
        crawler(names)
    done = [k for k, v in crawler.done.items() if v]
    failed = [k for k, v in crawler.done.items() if not v]
    with open('done.json', 'w') as result:
        json.dump(done, result)
    with open('failed.json', 'w') as result:
        json.dump(failed, result)


def create_database(args):
    from .models import create_database
    create_database()


def create_schema(args):
    from .models import create_schema
    create_schema()


def database_func(parser, args):
    if hasattr(args, 'dfunc'):
        args.dfunc(args)
    else:
        parser.print_help()


def void_func(args):
    voids_groups = void_list()
    keys = list(voids_groups.keys())
    print(len(keys))
    keys = limit(keys, args.first, args.last)
    voids_groups = {key: voids_groups[key] for key in keys}

    if args.async > 0:
        import asyncio
        from .async_void_crawler import AsyncVoidCrawler
        loop = asyncio.get_event_loop()
        crawler = AsyncVoidCrawler(loop, args.async)
        loop.run_until_complete(crawler(voids_groups))
    else:
        from .void_crawler import VoidCrawler
        crawler = VoidCrawler()
        crawler(voids_groups)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    datahub = subparsers.add_parser(
        'datahub', help='Buscar datasets no datahub')
    datahub.add_argument('-a', '--async', type=int, default=5,
                         help=("Número de requisições em paralelo no asyncio. "
                         "Se valor for 0, não usa asyncio"))
    datahub.add_argument('-c', '--cache', type=str, default='.list_cache.json',
                         help="Armazenar lista em cache")
    datahub.add_argument('-f', '--first', type=int, default=0,
                         help="Primeiro dataset: [first, last)")
    datahub.add_argument('-l', '--last', type=int, default=-1,
                         help="Ultimo dataset: [first, last). -1 indica último")
    datahub.set_defaults(func=datahub_func)

    database = subparsers.add_parser(
        'db', help='Database operations')
    dparsers = database.add_subparsers()
    dparsers.add_parser('create', help='Criar BD').set_defaults(
        dfunc=create_database)
    dparsers.add_parser('migrate', help='Criar tabelas').set_defaults(
        dfunc=create_schema)

    database.set_defaults(func=partial(database_func, database))


    void = subparsers.add_parser(
        'void', help='Buscar voids a partir de urls')
    void.add_argument('-a', '--async', type=int, default=5,
                         help=("Número de requisições em paralelo no asyncio. "
                         "Se valor for 0, não usa asyncio"))
    void.add_argument('-f', '--first', type=int, default=0,
                         help="Primeiro dataset: [first, last)")
    void.add_argument('-l', '--last', type=int, default=-1,
                         help="Ultimo dataset: [first, last). -1 indica último")
    void.set_defaults(func=void_func)


    args, _ = parser.parse_known_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

