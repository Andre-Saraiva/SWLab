from functools import partial
from .connection import create_database, connect
from .models import create_schema
from .queries import q_delete_empty_check_voids


def delete_empty_check_voids(args):
    with connect as conn:
        conn.execute(q_delete_empty_check_voids)


def database_func(parser, args):
    if hasattr(args, 'dfunc'):
        args.dfunc(args)
    else:
        parser.print_help()


def create_subparser(subparsers):
    database = subparsers.add_parser('db', help='Operações no BD')

    dparsers = database.add_subparsers()
    dparsers.add_parser('create', help='Criar BD').set_defaults(
        dfunc=lambda a: create_database())
    dparsers.add_parser('migrate', help='Criar tabelas').set_defaults(
        dfunc=lambda a: create_schema())
    dparsers.add_parser('delete_empty_check_voids',
        help='Remover check voids vazios').set_defaults(
        dfunc=delete_empty_check_voids)

    database.set_defaults(func=partial(database_func, database))
    return database
