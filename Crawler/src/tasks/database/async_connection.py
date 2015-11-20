'''
Created on 20/11/2015

@author: Joao Pimentel
'''
import asyncio
from aiopg.sa import create_engine
from .connection import USER, PASSWORD, HOST, DATABASE


@asyncio.coroutine
def engine():
    return (yield from create_engine(
        user=USER, database=DATABASE, host=HOST, password=PASSWORD))
