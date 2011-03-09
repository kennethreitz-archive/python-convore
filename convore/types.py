# -*- coding: utf-8 -*-
"""
    convore.types
    ~~~~~~~~~~~

    This module contains the reusable helper objects
    used throughout the wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""



class SyncedList(object):
    """Synced List datatype.

    __data_keys__ are the list of 'primary keys' for item lookup.
    self.get() needs to be defined.
    self.sync() needs to be defined.
    """

    __data_keys__ = ['id']

    def __init__(self):
        self.data = []
        #if hasattr(self, 'sync'):
        #    self.sync()


    def __repr__(self):
        return str(self.data)


    def __getitem__(self, key):

        if isinstance(key, int):
            key = unicode(key)

        for d in self.data:

            if key in [getattr(d, g) for g in self.__data_keys__]:
                return d

        if hasattr(self, 'get'):
            _fetched = self.get(key)
            if _fetched:
                self.data.append(_fetched)
                try:
                    if hasattr(self, 'parent'):
                        self.parent.data.append(_fetched)
                        if hasattr(self.parent, 'parent'):
                            self.parent.parent.data.append(_fetched)
                except AttributeError:
                    pass

                return _fetched


    def __iter__(self):
        for d in self.data:
            yield d


    def __len__(self):
        return len(self.data)


    def __contains__(self, key):

        if isinstance(key, int):
            key = unicode(key)

        for d in self.data:
            if key in [getattr(d, g) for g in self.__data_keys__]:
               return True

        return False
