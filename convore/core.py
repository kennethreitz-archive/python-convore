# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

from convore.packages.anyjson import deserialize
from types import SyncedList, ConvoreSyncedList
from api import Endpoints
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
        self.endpoints = Endpoints((username, password))

        self.groups = Groups(self.endpoints)

    def account_verify(self):
        r = self.endpoints.call(self.endpoints.account_verify)
        if r.has_key('error'):
            return False
        else:
            return True


    def fetch_live_data(self, cursor=''):
        return self.endpoints.call(self.endpoints.live, cursor=cursor)

    def live(self, cursor=''):
        messages = self.fetch_live_data(cursor)
        return self.import_live_from_api(messages)

    def import_live_from_api(self, messages):
        live_messages = list()
        next_cursor = ''
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


class Groups(ConvoreSyncedList):

    __data_keys__ = ['id', 'slug']

    def __init__(self, endpoints):
        super(Groups, self).__init__(endpoints)

        self.discover = groups.GroupsDiscover(endpoints)
        self.discover.parent = self

    def joined(self):
        """Returns list of Joined groups."""

        return [g for g in self.data if g.joined]

    def get(self, key):
        data = self.endpoints.call(self.endpoints.group_detail, group_id=key)
        group = self._create_group_from_api(data["group"])
        return group

    def sync(self):
        self.data = []

        data = self.endpoints.call(self.endpoints.groups)
        for _group in data['groups']:
            group = self._create_group_from_api(_group)
            self.data.append(group)
        self._synced = True

    def _create_group_from_api(self, _group):
        group = models.Group()
        group.import_from_api(_group)
        group.joined = True
        group.topics = Topics(group, self.endpoints)
        return group


class Topics(ConvoreSyncedList):

    __data_keys__ = ['id', 'slug']

    def __init__(self, group, endpoints):
        super(Topics, self).__init__(endpoints)
        self.group = group

    def list(self):
        return self.data

    def insert(self, index, object):
        return self.data.insert(index, object)

    def append(self, object):
        return self.data.append(object)

    def get(self, key):
        data = self.endpoints.call(self.endpoints.topic_detail, topic_id=key)
        topic = self._create_topic_from_api(data['topic'])
        return topic

    def sync(self):
        self.data = []

        data = self.endpoints.call(self.endpoints.group_topics, group_id=self.group.id)
        for _topic in data['topics']:
            topic = self._create_topic_from_api(_topic)
            self.data.append(topic)
        self._synced = True

    def _create_topic_from_api(self, _topic):
        topic = models.Topic()
        topic.import_from_api(_topic)
        topic.messages = Messages(topic, self.endpoints)
        topic.group = self.group
        return topic

    def create(self, name):
        params = {'topic_id': self.group.id, 'name': name}
        data = self.endpoints.call(self.endpoints.group_topic_create,
                           group_id=self.group.id,
                           name=name
                           )
        topic = self._create_topic_from_api(data['topic'])
        self.data.insert(0,topic)
        return True


class Messages(ConvoreSyncedList):

    __data_keys__ = ['id']

    def __init__(self, topic, auth):
        super(Messages, self).__init__(auth)
        self.topic = topic

    def list(self):
        return self.data

    def sync(self):
        self.data = []

        data = self.endpoints.call(self.endpoints.topic_messages,
                                   topic_id=self.topic.id
                                   )
        messages = data['messages']
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
        data = self.endpoints.call(self.endpoints.topic_message_create,
                           topic_id=self.topic.id,
                           message=message
                           )

        message = models.Message()
        message.import_from_api(data['message'])
        self.data.append(message)
        return True
