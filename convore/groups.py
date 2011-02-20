import json

import api
import models
from types import SyncedList


class GroupsDiscover(object):
    def __init__(self):
        self.explore = GroupsDiscoverExplore()
        self.explore.parent = self
        self.category = GroupDiscoverCategory()
        self.category.parent = self

    def _discover_group(self, *cats):
        _groups = []
        r = api.get('groups', 'discover', *cats)
        for group in json.loads(r.content)['groups']:
            _group = models.Group()
            _group.import_from_api(group)
            _groups.append(_group)

            #store into groups
            if not _group.id in self.parent:
                self.parent.data.append(_group)
                
        return _groups

    def friend(self):
        return self._discover_group('friend')

    # ^groups/discover/explore/(?P<angle>popular|recent|alphabetical).json


class GroupsDiscoverExplore(object):

    def _discover_group(self, *cats):
        _groups = []
        r = api.get('groups', 'discover', *cats)
        for group in json.loads(r.content)['groups']:
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
    pass
