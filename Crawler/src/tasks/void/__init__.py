from ..utils import limit
from .void_url import void_list


def _sync(args, voids_groups):
    from .void_crawler import VoidCrawler
    crawler = VoidCrawler()
    crawler(voids_groups)
    return crawler


def _async(args, voids_groups):
    import asyncio
    from .async_void_crawler import AsyncVoidCrawler
    loop = asyncio.get_event_loop()
    crawler = AsyncVoidCrawler(loop, args.async)
    #loop.set_debug(True)
    loop.run_until_complete(crawler(voids_groups))
    return crawler


def void_func(args):
    voids_groups = void_list()
    keys = list(voids_groups.keys())
    print(len(keys))
    keys = limit(keys, args.first, args.last)
    voids_groups = {key: voids_groups[key] for key in keys}
    print(len(keys), sum(len(v) for v in voids_groups.values()))

    (_async if args.async > 0 else _sync)(args, voids_groups)


def create_subparser(subparsers):
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
    return void
