'''
Created on 20/11/2015

@author: Joao Pimentel
'''
import tqdm

def limit(collection, first, last):
    last = last if last != -1 else len(collection)
    if last < first:
        first = first - 1 if first else None
        last = last - 1
        collection = collection[last:first:-1]
    else:
        collection = collection[first:last]
    return collection

def progress(iterable, total=None):
    if total is None and hasattr(iterable, '__len__'):
        total = len(iterable)
    for value in tqdm.tqdm(iterable, total=total):
        yield value