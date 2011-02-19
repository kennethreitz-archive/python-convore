# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""
import json

import requests

import models
import api


__title__ = 'convore'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'


API_URL = 'https://convore.com/api/'


def login(username, password):
    api.login(username, password)

    
def account_verify():
    r = requests.get(API_URL + 'account/verify.json')
    try:
        r.raise_for_status()
        if r.status_code == 200:
            return True
        else:
            return False
    except requests.HTTPError:
        raise LoginFailed


def groups(group_id=None):
    # seeking list of groups
    try:

        if not group_id:
            r = requests.get(API_URL + 'groups.json')
            groups = json.loads(r.content)['groups']

            _groups = []
            
            for group in groups:
                _group = models.Group()
                _group.import_from_api(group)
                _groups.append(_group)


            return _groups
        # seeking unique group
        else:

            pass
    except requests.HTTPError:
        raise LoginFailed



class LoginFailed(RuntimeError):
    """Login falied!"""
