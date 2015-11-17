'''
Created on 16/11/2015

@author: Joao Pimentel
'''
import requests
import os
import json

def load_datahub_list(use_cache=False):
    if use_cache and os.path.exists('.list_cache.json'):
        with open('.list_cache.json', 'r') as cache:
            return json.load(cache)
        
    resp = requests.get('http://datahub.io/api/rest/dataset')
    if resp.status_code == 200:
        result = resp.json()
        with open('.list_cache.json', 'w') as cache:
            json.dump(result, cache)
        return result
