'''
Created on 20/11/2015

@author: Joao Pimentel
'''
import asyncio
import tqdm

@asyncio.coroutine
def wait_with_progress(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f
