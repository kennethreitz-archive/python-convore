import requests
import json
import models

from UserList import UserList

API_URL = 'https://convore.com/api/'

def login(username, password):
    auth = requests.AuthObject(username, password)
    requests.add_autoauth(API_URL, auth)
    

class Groups(UserList):
    
    def __init__(self):
        self.data = []
        self.sync()


    def __getitem__(self, key):

        if isinstance(key, int):
            key = unicode(key)

        for group in self.data:
            if key in (group.id, group.slug):
               return group

    def __contains__(self, key):
        
        if isinstance(key, int):
            key = unicode(key)

        for group in self.data:
            if key in (group.id, group.slug):
               return True

        return False

    def __iter__(self):
        for group in self.data:
            yield group

    def sync(self):

        self.data = []

        r = requests.get(API_URL + 'groups.json')
        for _group in json.loads(r.content)['groups']:

            group = models.Group()
            group.import_from_api(_group)
            self.data.append(group)
