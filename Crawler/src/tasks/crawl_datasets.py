'''
Created on 03/11/2015

@author: Luiz Leme
'''

import argparse

from . import datahub
from . import database
from . import void
from . import resources


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    datahub.create_subparser(subparsers)
    database.create_subparser(subparsers)
    void.create_subparser(subparsers)
    resources.create_subparser(subparsers)

    args, _ = parser.parse_known_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
