# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

from convore.packages.anyjson import deserialize

import api
import models


__title__ = 'convore'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'
__docformat__ = 'restructuredtext'

__all__ = ('Convore',)


LIVE_TYPES = {
    'read': models.Read,
    'message': models.Message,
    'topic': models.Topic,
    'login': models.Login,
    'logout': models.Logout,
}

class Convore(object):
    """The main Convore interface object."""

    def __init__(self, username, password):
        self.username = username
        api.login(username, password)

        self.groups = api.Groups()

    def account_verify(self):
        r = api.get('account', 'verify')
        if r.status_code == 200:
            return True
        else:
            return False


    def fetch_live_data(self, cursor=None):
        params= {}

        if cursor <> None:
            params['cursor'] = cursor

        r = api.get('live', params=params)
        return deserialize(r.content)['messages']

    def live(self, cursor=None):
        messages = self.fetch_live_data(cursor)
        (live_messages, next_cursor) = self.import_live_from_api(messages)

        return (live_messages, next_cursor)

    def import_live_from_api(self, messages):
        live_messages = list()
        next_cursor = None
        for data in messages:
            try:
                class_ = LIVE_TYPES[data['kind']]
            except KeyError:
                continue

            message = class_()
            message.import_from_api(data)

            if data['kind'] == 'topic':
                message.group_id = data['group']
            elif data['kind'] == 'message':
                message.group_id = data['group']
                message.topic = models.LiveTopic()
                message.topic.import_from_api(data['topic'])

            live_messages.append({'kind': data['kind'],
                                  'message': message})
            next_cursor = data['_id']

        return (live_messages, next_cursor)
