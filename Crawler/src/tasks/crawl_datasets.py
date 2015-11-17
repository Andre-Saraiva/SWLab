'''
Created on 03/11/2015

@author: Luiz Leme
'''

import argparse
from .load_list import load_datahub_list
from functools import partial

def datahub_func(args):
    names = load_datahub_list(args.cache)
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
    with open('done.txt', 'a') as result:
        result.write('\n'.join(done))
    with open('failed.txt', 'a') as result:
        result.write('\n'.join(failed))


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

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    datahub = subparsers.add_parser(
        'datahub', help='Buscar datasets no datahub')
    datahub.add_argument('-a', '--async', type=int, default=5,
                         help=("Número de requisições em paralelo no asyncio. "
                         "Se valor for 0, não usa asyncio"))
    datahub.add_argument('-c', '--cache', action='store_true', default=True,
                         help="Armazenar lista em cache")
    datahub.set_defaults(func=datahub_func)
    
    database = subparsers.add_parser(
        'db', help='Database operations')
    dparsers = database.add_subparsers()
    dparsers.add_parser('create', help='Criar BD').set_defaults(
        dfunc=create_database)
    dparsers.add_parser('migrate', help='Criar tabelas').set_defaults(
        dfunc=create_schema)

    database.set_defaults(func=partial(database_func, database))

    args, _ = parser.parse_known_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

