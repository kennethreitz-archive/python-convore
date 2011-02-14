# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

import requests


__title__ = 'convore'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'



API_URL = 'https://convore.com/api/'


class Convore(object):
	"""The :class:`Convore` object is the heart of this api wrapper. It
	provides all core functionality.

    :param username: Username to authenticate with.
    :param password: Password for given username.
    
	"""

	def __init__(self, username, password):
		self.username = username
		self.password = password

		requests.add_autoauth(API_URL, requests.AuthObject(self.username, self.password))

		self.verify()

	def verify(self):
		"""Authenticates. Returns True if authentication is successful, False if not."""

		r = requests.get(API_URL + 'account/verify.json')

		return True if r.status_code == 200 else False
	
		
class Groups(object):
	def create(self):
		pass

	
class Group(object):
	pass
	def __init__(self, id):
		pass

	def leave(self):
		pass
