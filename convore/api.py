# -*- coding: utf-8 -*-
"""
    convore.api
    ~~~~~~~~~~~

    This module implements the Convore API wrapper objects.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

import json
from datetime import datetime

import requests


API_URL = 'https://convore.com/api/'


# =======
# Helpers
# =======

def _safe_response(r):
    print r
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
    print r.url
   
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
        self.friends = None
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

        self.friends = []
        
        if 'friend_list' in d:
            for friend in d.get('friend_list', None):
                _user = User()
                _user.import_from_api(friend)
                self.friends.append(_user)


    def __repr__(self):
        return '<group %s>' % (self.slug)    



# ==========
# End Points
# ==========


class Groups(SyncedList):

    def __init__(self):
        super(Groups, self).__init__()

        self.sync()
        self.discover = GroupsDiscover()

    def joined(self):
        """Returns list of Joined groups."""

        return [g for g in self.data if g.joined]
        

    def __getitem__(self, key):

        for group in self.data:

            if str(key) in [group.id, group.slug]:
               return group
            
        r = get('groups', key)

        _group = Group()
        _group.import_from_api(json.loads(r.content)['group'])
        self.data.append(_group)
        
        return _group

    def __contains__(self, key):
        
        if isinstance(key, int):
            key = unicode(key)

        for group in self.data:
            if key in [group.id, group.slug]:
               return True

        return False


    def sync(self):

        self.data = []

        r = requests.get(API_URL + 'groups.json')
        for _group in json.loads(r.content)['groups']:

            group = Group()
            group.import_from_api(_group)
            group.joined = True
            self.data.append(group)


            
class GroupsDiscover(object):
    def __init__(self):
        self.explore = GroupsDiscoverExplore()
        self.category = GroupDiscoverCategory()

    def _discover_group(self, *cats):
        _groups = []
        r = get('groups', 'discover', *cats)
        for group in json.loads(r.content)['groups']:
            _group = Group()
            _group.import_from_api(group)
            _groups.append(_group)
        return _groups

    def friend(self):
        return self._discover_group('friend')

    # ^groups/discover/explore/(?P<angle>popular|recent|alphabetical).json


class GroupsDiscoverExplore(object):

    def _discover_group(self, *cats):
        _groups = []
        r = get('groups', 'discover', *cats)
        for group in json.loads(r.content)['groups']:
            _group = Group()
            _group.import_from_api(group)
            _groups.append(_group)
        return _groups

    def popular(self):
        return self._discover_group('explore', 'popular')

    def recent(self):
        return self._discover_group('explore', 'recent')

    def alphabetical(self):
        return self._discover_group('explore', 'alphabetical')

class GroupDiscoverCategory(SyncedList):
    pass
        


#^groups/discover/friend.json
#^groups/discover/explore/(?P<angle>popular|recent|alphabetical).json
#^groups/discover/category.json
#^groups/discover/category/(?P<category>[\w-]+).json
#^groups/discover/search.json
#^groups/(?P<group_id>\d+)/join.json
#^groups/(?P<group_id>\d+)/request.json





