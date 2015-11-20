'''
Created on 20/11/2015

@author: Joao Pimentel
'''
def extra_links(extras):
    for key, value in extras.items():
        if key.startswith('links:'):
            yield (key[6:], value)


def relationships(relations):
    for relationship in relations:
        if relationship['type'] == 'links_to':
            yield relationship


def update_done(done, name):
    with open('done.txt' if done[name] else 'failed.txt', 'a') as fil:
        fil.write(name + '\n')
