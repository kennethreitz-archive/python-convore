# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

from convore.packages.anyjson import deserialize

from types import SyncedList
import api
import models
import groups


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

        self.groups = Groups()

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
        r = api.get('groups', key)
        group = self._create_group_from_api(deserialize(r.content)['group'])
        return group

    def sync(self):
        self.data = []

        r = api.get('groups')
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
        r = api.get('topics', key)
        topic = self._create_topic_from_api(deserialize(r.content)['topic'])
        return topic

    def sync(self):
        self.data = []

        r = api.get('groups', self.group.id, 'topics')
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

        r = api.get('topics', self.topic.id, 'messages')
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

