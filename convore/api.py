# -*- coding: utf-8 -*-
"""
    convore.api
    ~~~~~~~~~~~

    This module implements the Convore API wrapper objects.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

import json

import requests

from types import SyncedList
import models
import groups



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
    """Configured API Credentials"""
    auth = requests.AuthObject(username, password)
    requests.add_autoauth(API_URL, auth)


# ==========
# End Points
# ==========


class Groups(SyncedList):

    __data_keys__ = ['id', 'slug']

    def __init__(self):
        super(Groups, self).__init__()

        self.discover = groups.GroupsDiscover()
        self.discover.parent = self

    def joined(self):
        """Returns list of Joined groups."""

        return [g for g in self.data if g.joined]


    def get(self, key):
        r = get('groups', key)

        group = models.Group()
        group.import_from_api(json.loads(r.content)['group'])
        return group

    def sync(self):

        self.data = []

        r = get('groups')
        for _group in json.loads(r.content)['groups']:

            group = models.Group()
            group.import_from_api(_group)
            group.joined = True
            self.data.append(group)


            

        


#^groups/discover/friend.json
#^groups/discover/explore/(?P<angle>popular|recent|alphabetical).json
#^groups/discover/category.json
#^groups/discover/category/(?P<category>[\w-]+).json
#^groups/discover/search.json
#^groups/(?P<group_id>\d+)/join.json
#^groups/(?P<group_id>\d+)/request.json





