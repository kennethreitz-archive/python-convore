import requests
import json
import models

API_URL = 'https://convore.com/api/'

def login(username, password):
    auth = requests.AuthObject(username, password)
    requests.add_autoauth(API_URL, auth)
    

class Groups(object):
    
    
    def __init__(self):
        pass
        
        
    def __iter__(self):
        r = requests.get(API_URL + 'groups.json')
        groups = json.loads(r.content)['groups']
        
        for group in groups:
            _group = models.Group()
            _group.import_from_api(group)
            yield _group

    def __getitem__(self, key):
        r = requests.get(API_URL + 'groups/%s.json' % key)
        group = models.Group()
        _group = json.loads(r.content)['group']
        group.import_from_api(_group)

        return _group
        
    def iterkeys():
        return []
        
    def iteritems():
        return
