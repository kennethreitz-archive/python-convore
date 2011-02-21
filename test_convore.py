#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    convore tests
    ~~~~~~~~~~~~~

    Convore test suite.

    Looks for authentication in 'CONVORE_NAME' and
    'CONVORE_PASS' environment variables.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""


import os
import unittest

import convore


CONVORE_NAME = os.environ.get('CONVORE_NAME', 'requeststest')
CONVORE_PASS = os.environ.get('CONVORE_PASS', 'requeststest')


class ConvoreAPI(unittest.TestCase):
    """Requests test cases."""
    
    def setUp(self):
        self.convore = convore.Convore(CONVORE_NAME, CONVORE_PASS)

    def tearDown(self):
        pass

    def test_convore_login(self):
        self.assertEqual(self.convore.account_verify(), True)





class ConvoreGroups(unittest.TestCase):
    def setUp(self):
        self.convore = convore.Convore(CONVORE_NAME, CONVORE_PASS)
        
    def test_works(self):
        self.convore.groups

    def test_cache_works(self):
        int_before = int(len(self.convore.groups))

        self.convore.groups[81]

        int_after = int(len(self.convore.groups))
        self.assertEqual((int_after - int_before), 1)

    def test_discover_explore(self):
        self.convore.groups.discover.explore.popular()
        self.convore.groups.discover.explore.recent()
        self.convore.groups.discover.explore.alphabetical()


    def test_discover_category(self):
        self.convore.groups.discover.category

        c = self.convore.groups.discover.category['gossip']
        self.assertIsInstance(c, convore.models.Category)



if __name__ == '__main__':
    unittest.main()
