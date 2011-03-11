# -*- coding: utf-8 -*-
"""
    convore.models
    ~~~~~~~~~~~~~~

    This module implements the internal models for
    Convore API object storage.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

from datetime import datetime



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


class Topic(object):
    """Convore topic object"""

    def __init__(self):
        self.id = None
        self.name = None
        self.slug = None
        self.url = None
        self.message_count = None
        self.unread = None
        self.date_created = None
        self.date_latest_message = None
        self.creator = None


    def import_from_api(self, data):
        self.creator = User()

        self.id = data.get('id', None)
        self.name = data.get('name', None)
        self.slug = data.get('slug', None)
        self.url = data.get('url', None)
        self.message_count = data.get('message_count', None)
        self.unread = data.get('unread', None)
        self.date_created = datetime.utcfromtimestamp(
                data.get('date_created', None)
        )
        self.date_latest_message = datetime.utcfromtimestamp(
                data.get('date_latest_message', None)
        )
        self.creator.import_from_api(data.get('creator', None))


class Message(object):
    """Convore message object"""

    def __init__(self):
        self.id = None
        self.message = None
        self.date_created = None
        self.user = None


    def import_from_api(self, data):
        self.user = User()

        self.id = data.get('id', None)
        self.message = data.get('message', None)
        self.date_created = datetime.utcfromtimestamp(
                data.get('date_created', None)
        )
        self.user.import_from_api(data.get('user', None))


class Category(object):
    def __init__(self):
        self.groups_count = None
        self.slug = None
        self.name = None
        self.groups = None

    def __repr__(self):
        return '<category %s>' % (self.slug)

    def import_from_api(self, d):
        """Constructs Category from deserialized API Response."""
        self.groups_count = d.get('groups_count', None)
        self.slug = d.get('slug', None)
        self.name = d.get('name', None)


class Read(object):
    def __init__(self):
        self.topic = None
        self.when  = None
        self.user  = None

    def import_from_api(self, data):
        """Constructs object from deserialized API Response."""
        self.when  = datetime.utcfromtimestamp(
                data.get('_ts', None)
        )
        self.user  = User()
        self.user.import_from_api(data.get('user', None))


class Login(object):
    def __init__(self):
        self.when  = None
        self.user  = None

    def import_from_api(self, data):
        """Constructs object from deserialized API Response."""
        self.when  = datetime.utcfromtimestamp(
                data.get('_ts', None)
        )
        self.user  = User()
        self.user.import_from_api(data.get('user', None))


class Logout(object):
    def __init__(self):
        self.when  = None
        self.user  = None

    def import_from_api(self, data):
        """Constructs object from deserialized API Response."""
        self.when  = datetime.utcfromtimestamp(
                data.get('_ts', None)
        )
        self.user  = User()
        self.user.import_from_api(data.get('user', None))
