'''
Created on 16/11/2015

@author: Joao Pimentel
'''
import requests
import os
import json

def load_datahub_list(cache='.list_cache.json'):
    if cache and os.path.exists(cache):
        with open(cache, 'r') as cachef:
            return json.load(cachef)
        
    resp = requests.get('http://datahub.io/api/rest/dataset')
    if resp.status_code == 200:
        result = resp.json()
        if cache:
            with open(cache, 'w') as cachef:
                json.dump(result, cachef)
        return result
