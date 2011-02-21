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
    def __init__(self):
        self.explore = GroupsDiscoverExplore()
        self.explore.parent = self
        self.category = GroupDiscoverCategory()
        self.category.parent = self

    def _discover_group(self, *cats):
        _groups = []
        r = api.get('groups', 'discover', *cats)
        for group in deserialize(r.content)['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

            #store into groups
            if not _group.id in self.parent:
                self.parent.data.append(_group)
                
        return _groups

    def friend(self):
        return self._discover_group('friend')


class GroupsDiscoverExplore(object):

    def _discover_group(self, *cats):
        _groups = []
        r = api.get('groups', 'discover', *cats)
        for group in deserialize(r.content)['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

            #store into groups
            if not _group.id in self.parent.parent:
                self.parent.parent.data.append(_group)

        return _groups

    def popular(self):
        return self._discover_group('explore', 'popular')

    def recent(self):
        return self._discover_group('explore', 'recent')

    def alphabetical(self):
        return self._discover_group('explore', 'alphabetical')

    def __repr__(self):
        return '<convore groups/discover/explore endpoint>'


class GroupDiscoverCategory(SyncedList):

    __data_keys__ = ['slug',]

    def __init__(self):
        super(GroupDiscoverCategory, self).__init__()

    def get(self, key):
        r = api.get('groups', 'discover', 'category', key)
        print r.content
        cat = models.Category()
        cat.import_from_api(deserialize(r.content)['categories'])
        return cat

    def sync(self):
        r = api.get('groups', 'discover', 'category')
        for _cat in deserialize(r.content)['categories']:
            cat = models.Category()
            cat.import_from_api(_cat)
            self.data.append(cat)
