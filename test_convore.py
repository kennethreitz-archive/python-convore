#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import convore


class ConvoreTestSuite(unittest.TestCase):
    """Requests test cases."""
    
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convore_login(self):
        _convore = convore.Convore('requeststest', 'requeststest')
        self.assertEqual(_convore.account_verify(), True)

    


if __name__ == '__main__':
    unittest.main()
