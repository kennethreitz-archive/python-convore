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


class Category(object):
    def __init__(self):
        self.groups_count = None
        self.slug = None
        self.name = None

    def __repr__(self):
        return '<category %s>' % (self.slug)

    def import_from_api(self, d):
        """Constructs Category from deserialized API Response."""
        self.groups_count = d.get('groups_count', None)
        self.slug = d.get('slug', None)
        self.name = d.get('name', None)
