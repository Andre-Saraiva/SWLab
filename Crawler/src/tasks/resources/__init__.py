from functools import partial
from .cache_voids import update_description, crawler, void_resources


def cache(args):
    voids = void_resources()
    crawler(voids)


def resources_func(parser, args):
    if hasattr(args, 'rfunc'):
        args.rfunc(args)
    else:
        parser.print_help()


def create_subparser(subparsers):
    resources = subparsers.add_parser('resources',
        help='Operações em recursos')

    rparsers = resources.add_subparsers()
    rparsers.add_parser('normalize',
        help='Normalizar coluna description de resources').set_defaults(
        rfunc=lambda a: update_description())
    rparsers.add_parser('cache',
        help='Carregar voids e salvar no BD').set_defaults(
        rfunc=cache)

    resources.set_defaults(func=partial(resources_func, resources))
    return resources
