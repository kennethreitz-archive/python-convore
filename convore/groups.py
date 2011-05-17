# -*- coding: utf-8 -*-
"""
    convore.groups
    ~~~~~~~~~~~

    This module implements the group endpoint sub-wrappers.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""
import api
import models
from convore.packages.anyjson import deserialize
from convore.types import SyncedList

class GroupsDiscover(object):
    def __init__(self, endpoints=None):
        self.explore = GroupsDiscoverExplore()
        self.explore.parent = self
        self.category = GroupDiscoverCategory()
        self.category.parent = self
        self.endpoints = endpoints
        isinstance(self.endpoints, api.Endpoints)

    def friend(self):
        _groups = []
        r = self.endpoints.call(self.endpoints.discover_groups_by_friend,
                                category=cats
                                )

        for group in r['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

            #store into groups
            if not _group.id in self.parent:
                self.parent.data.append(_group)

        return _groups

    @staticmethod
    def search(key):
        _groups = []

        r = api.Endpoints.discover_groups_by_search.call(q=key)
        for group in r['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

        return _groups


class GroupsDiscoverExplore(object):

    def _discover_group(self, cats):
        _groups = []
        r = api.Endpoints.discover_groups_explore.call(sort=cats)
        for group in r['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

            #store into groups
            if not _group.id in self.parent.parent:
                self.parent.parent.data.append(_group)

        return _groups

    def popular(self):
        return self._discover_group('popular')

    def recent(self):
        return self._discover_group('recent')

    def alphabetical(self):
        return self._discover_group('alphabetical')

    def __repr__(self):
        return '<convore groups/discover/explore endpoint>'


class GroupDiscoverCategory(SyncedList):

    __data_keys__ = []

    def __init__(self):
        super(GroupDiscoverCategory, self).__init__()

    def get(self, key):

        error = 'Invalid group slug given.'

        r = self.endpoints.call(api.Endpoints.discover_groups_by_category, category_slug=key)

        groups = r['groups']

        i = [c.slug for c in self.data].index(key)
        self.data[i].groups = groups

        return self.data[i]


    def sync(self):
        r = self.endpoints.call(api.Endpoints.discover_categories)
        r = api.get('groups', 'discover', 'category')
        for _cat in deserialize(r.content)['categories']:
            cat = models.Category()
            cat.import_from_api(_cat)
            self.data.append(cat)


