# -*- coding: utf-8 -*-
"""
    convore.api
    ~~~~~~~~~~~

    This module implements the Convore API wrapper objects.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

from convore.packages.anyjson import deserialize

import requests

from types import SyncedList
import models
import groups



API_URL = 'https://convore.com/api/'
AUTH = None

# =======
# Helpers
# =======

def _safe_response(r, error=None):
    try:
        r.raise_for_status()
        return r
    except requests.HTTPError:
        if r.status_code == 401:
            raise LoginFailed
        else:
            raise APIError(error) if error else APIError


def get(*path, **kwargs):
    """
    Accepts optional error parameter, which will be passed in the event of a
    non-401 HTTP error.

    api.get('groups')
    api.get('groups', 'id')
    api.get('accounts', 'verify')
    """
    url =  '%s%s%s' % (API_URL, '/'.join(map(str, path)), '.json')

    params = kwargs.get('params', None)

    r = requests.get(url, params=params, auth=auth)

    error = kwargs.get('error', None)
    return _safe_response(r, error)


def post(params, *path):

    url =  '%s%s%s' % (API_URL, '/'.join(map(str, path)), '.json')
    r = requests.post(url, data=params, auth=auth)
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
    global auth

    auth = (username, password)
    # print requests.auth_manager.__dict__

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
        group = self._create_group_from_api(deserialize(r.content)['group'])
        return group

    def sync(self):
        self.data = []

        r = get('groups')
        for _group in deserialize(r.content)['groups']:
            group = self._create_group_from_api(_group)
            self.data.append(group)
        self._synced = True

    def _create_group_from_api(self, _group):
        group = models.Group()
        group.import_from_api(_group)
        group.joined = True
        group.topics = Topics(group)
        return group


class Topics(SyncedList):

    __data_keys__ = ['id', 'slug']

    def __init__(self, group):
        super(Topics, self).__init__()
        self.group = group

    def list(self):
        return self.data

    def insert(self, index, object):
        return self.data.insert(index, object)

    def append(self, object):
        return self.data.append(object)

    def get(self, key):
        r = get('topics', key)
        topic = self._create_topic_from_api(deserialize(r.content)['topic'])
        return topic

    def sync(self):
        self.data = []

        r = get('groups', self.group.id, 'topics')
        for _topic in deserialize(r.content)['topics']:
            topic = self._create_topic_from_api(_topic)
            self.data.append(topic)
        self._synced = True

    def _create_topic_from_api(self, _topic):
        topic = models.Topic()
        topic.import_from_api(_topic)
        topic.messages = Messages(topic)
        topic.group = self.group
        return topic

    def create(self, name):
        params = {'topic_id': self.group.id, 'name': name}
        r = post(params ,'groups', self.group.id, 'topics', 'create')
        topic = self._create_topic_from_api(deserialize(r.content)['topic'])
        self.data.insert(0,topic)
        return True


class Messages(SyncedList):

    __data_keys__ = ['id']

    def __init__(self, topic):
        super(Messages, self).__init__()
        self.topic = topic

    def list(self):
        return self.data

    def sync(self):
        self.data = []

        r = get('topics', self.topic.id, 'messages')
        messages = deserialize(r.content)['messages']
        idx = 0
        msg_count = len(messages)
        unread_count = self.topic.unread
        for message_data in messages:
            idx = idx + 1
            message = models.Message()
            message.import_from_api(message_data)
            message.topic = self.topic
            message.unread = idx > msg_count - unread_count
            self.data.append(message)
        self._synced = True

    def create(self, message):
        params = {'topic_id': self.topic.id, 'message': message}
        r = post(params ,'topics', self.topic.id, 'messages', 'create')
        message = models.Message()
        message.import_from_api(deserialize(r.content)['message'])
        self.data.append(message)
        return True
