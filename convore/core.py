# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

import api


__title__ = 'convore'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'


API_URL = 'https://convore.com/api/'

class Convore(object):
    def __init__(self, username, password):
        self.username = username

        api.login(username, password)

    @property
    def groups(self):
        return api.Groups()

    def account_verify(self):

        r = requests.get(API_URL + 'account/verify.json')
        try:
            r.raise_for_status()
            if r.status_code == 200:
                return True
            else:
                return False
        except requests.HTTPError:
            raise LoginFailed


        
class LoginFailed(RuntimeError):
    """Login falied!"""
