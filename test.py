#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from convore import Convore


CONVORE_NAME = os.environ.get('CONVORE_NAME', 'requeststest')
CONVORE_PASS = os.environ.get('CONVORE_PASS', 'requeststest')

convore = Convore(CONVORE_NAME, CONVORE_PASS)

#print convore.groups.discover.category
convore.groups.discover.search('github')
