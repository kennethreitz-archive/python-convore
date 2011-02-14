# -*- coding: utf-8 -*-
"""
	convore.request
	~~~~~~~~~~~~~~~

	This module implements the main Convore request system.

	:copyright: (c) 2011 by Kenneth Reitz.
	:license: ISC, see LICENSE for more details.
"""

import sys

try:
	import simplejson as json
except ImportError:
	import json

import requests


URL_PREFIX = "https://convore.com/api/"


class ConvoreRequest(object):
	convore_url = CONVORE_URL
	ConvoreError = ConvoreError

	def __init__(self, username, password):
		self.username = username
		self.password = password

class ConvoreError(Exception):
	"""An error occured while making a request to the Convore API."""
