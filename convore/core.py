# -*- coding: utf-8 -*-
"""
    convore.core
    ~~~~~~~~~~~

    This module implements the main Convore wrapper.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""



__title__ = 'convore'
__version__ = '0.0.1'
__build__ = 0x000001
__author__ = 'Kenneth Reitz'
__license__ = 'ISC'
__copyright__ = 'Copyright 2011 Kenneth Reitz'



class Convore(object):
	"""The :class:`Convore` object is the heart of this api wrapper. It
	provides all core functionality.

    :param username: Username to authenticate with.
    :param password: Password for given username.
    
	"""

	def __init__(self, username, password):
		
		self.verify()

	def verify(self):
		"""Authenticates. Returns True if authentication is successful, False if not."""
		pass
		

class AuthorizationFailed(Exception):
	"Your given username/password was denied access."
