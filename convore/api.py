import json
from datetime import datetime
from UserList import UserList

import requests



API_URL = 'https://convore.com/api/'

# =======
# Helpers
# =======

def _safe_response(r):
    try:
        r.raise_for_status()
        return r
    except requests.HTTPError:
        if r.status_code == 401:
            raise LoginFailed
        else:
            raise APIError

def get(*path):
    """
    api.get('groups')
    api.get('groups', 'id')
    api.get('accounts', 'verify')
    """
    
    url =  '%s%s%s' % (API_URL, '/'.join(map(str, path)), '.json')
    r = requests.get(url)
    return _safe_response(r)


def post(params, *path):
    url =  '%s%s%s' % (API_URL, '/'.join(map(str, path)), '.json')
    r = requests.post(url, params=params)
    return _safe_response(r)

# ==========
# Exceptions
# ==========

class LoginFailed(RuntimeError):
    """Login falied!"""

class APIError(RuntimeError):
    """There was a problem properly accessing the Convore API."""



def login(username, password):
    auth = requests.AuthObject(username, password)
    requests.add_autoauth(API_URL, auth)
    
# ======
# Models
# ======

class User(object):
    """Convore User object."""

    def __init__(self):
        self.username = None
        self.url = None
        self.id = None
        self.img = None

    def import_from_api(self, d):
        """Constructs User from Deserialized API Response."""
        self.username = d.get('username', None)
        self.url = d.get('url', None)
        self.id = d.get('id', None)
        self.img = d.get('img', None)

    def __repr__(self):
        return '<user @%s>' % (self.username)

    
class Group(object):
    """Convore Group object."""

    def __init__(self):
        self.kind = None
        self.members_count = None
        self.name = None
        self.creator = None
        self.url = None
        self.slug = None
        self.date_latest_message = None
        self.date_created = None
        self.topics_count = None
        self.unread = None
        self.id = None
        self.joined = False

    def import_from_api(self, d):
        """Constructs Group from Deserialized API Response."""

        self.creator = User()

        self.kind = d.get('kind', None)
        self.members_count = d.get('members_count', None)
        self.name = d.get('name', None)
        self.creator.import_from_api(d.get('creator', None))
        self.url = d.get('url', None)
        self.slug = d.get('slug', None)
        self.date_latest_message = datetime.utcfromtimestamp(
                d.get('date_latest_message', None)
        )
        self.date_created = datetime.utcfromtimestamp(
                d.get('date_created', None)
        )
        self.topics_count = d.get('topics_count', None)
        self.unread = d.get('unread', None)
        self.id = d.get('id', None)

    def __repr__(self):
        return '<group %s>' % (self.slug)    



# ==========
# End Points
# ==========


class Groups(UserList):
    
    def __init__(self):
        self.data = []
        self.sync()

    def joined(self):
        """Returns list of Joined groups."""

        return [g for g in self.data if g.joined]

    def __getitem__(self, key):

        if isinstance(key, int):
            key = unicode(key)

        for group in self.data:
            if key in (group.id, group.slug):
               return group

        try:
            r = get('groups', key)

            group = Group()
            group.import_from_api(json.loads(r.content)['group'])

            self.data.append(group)
            return group
        
        except requests.HTTPError:
            return None


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

            group = Group()
            group.import_from_api(_group)
            group.joined = True
            self.data.append(group)


