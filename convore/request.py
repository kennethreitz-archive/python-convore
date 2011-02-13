# -*- coding: utf-8 -*-
"""
	convore.request
	~~~~~~~~~~~~~~~

	This module implements the main Convore request system.

	:copyright: (c) 2011 by Kenneth Reitz.
	:license: ISC, see LICENSE for more details.
"""

import sys
import httplib
try:
	import simplejson as json
except ImportError:
	import json

from urlparse import urlparse, urlunparse
try:
	from urlparse import parse_qs
except ImportError:
	from cgi import parse_qs
from urllib import urlencode



CONVORE_URL = "https://convore.com"
URL_PREFIX = "https://convore.com/api/"


class ConvoreError(Exception):
	"""An error occured while making a request to the Convore API."""


class ConvoreRequest(object):
	convore_url = CONVORE_URL
	url_format = "%(convore_url)s/api/%(api_format)s"
	api_format = "json"
	ConvoreError = ConvoreError

	def __init__(self, username, password, url_prefix=None):
		self.username = username
		self.password = password

		if not self.url_prefix:
			self.url_prefix = self.url_format % {
				'convore_url': self.convore_url,
				'api_format': self.api_format
			}

	def get(self, *path_components):
		path_components = filter(None, path_components)

	def post(self, *path_components, **extra_post_data):
		return self.make_request("/".join(path_components), extra_post_data,
			method="POST")

	def make_request(self, path, extra_post_data=None, method="GET"):
		extra_post_data = extra_post_data or {}
		url = "/".join([self.url_prefix, path])
		return self.raw_request(url, extra_post_data, method=method)

