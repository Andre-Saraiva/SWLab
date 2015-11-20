import json
from ..utils import limit
from .load_list import load_datahub_list


def _sync(args, names):
    from .sync_crawler import SyncCrawler
    crawler = SyncCrawler()
    crawler(names)
    return crawler


def _async(args, names):
    import asyncio
    from .async_crawler import AsyncCrawler
    loop = asyncio.get_event_loop()
    crawler = AsyncCrawler(loop, args.async)
    loop.run_until_complete(crawler(names))
    return crawler


def datahub_func(args):
    names = load_datahub_list(args.cache)
    print(len(names))
    names = limit(names, args.first, args.last)
    print(len(names))

    crawler = (_async if args.async > 0 else _sync)(args, names)

    done = [k for k, v in crawler.done.items() if v]
    failed = [k for k, v in crawler.done.items() if not v]
    with open('done.json', 'w') as result:
        json.dump(done, result)
    with open('failed.json', 'w') as result:
        json.dump(failed, result)


def create_subparser(subparsers):
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
    return datahub
