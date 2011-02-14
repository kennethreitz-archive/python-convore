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

	def get(self, *path_components):
		path_components = filter(None, path_components)

	def post(self, *path_components, **extra_post_data):
		return self.make_request("/".join(path_components), extra_post_data,
			method="POST")

	def make_request(self, path, extra_post_data=None, method="GET"):
		extra_post_data = extra_post_data or {}
		url = "/".join([self.url_prefix, path])
		return self.raw_request(url, extra_post_data, method=method)

class ConvoreError(Exception):
	"""An error occured while making a request to the Convore API."""
