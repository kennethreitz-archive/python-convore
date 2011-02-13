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
	"""The :class:`Convore` object is the heart of this api wrapper. It provides all core
    functionality.

    # Usually you create a :class:`Dataset` instance in your main module, and append
    #    rows and columns as you collect data. ::
    # 
    #        data = tablib.Dataset()
    #        data.headers = ('name', 'age')
    # 
    #        for (name, age) in some_collector():
    #            data.append((name, age))
    # 
    #    You can also set rows and headers upon instantiation. This is useful if dealing
    #    with dozens or hundres of :class:`Dataset` objects. ::
    # 
    #        headers = ('first_name', 'last_name')
    #        data = [('John', 'Adams'), ('George', 'Washington')]
    # 
    #        data = tablib.Dataset(*data, headers=headers)


    :param username: Username to authenticate with.
    :param password: Password for given username.


    # .. admonition:: Format Attributes Definition
    # 
    #   If you look at the code, the various output/import formats are not
    #   defined within the :class:`Dataset` object. To add support for a new format, see
    #   :ref:`Adding New Formats <newformats>`.

	"""

	def __init__(self, username, password):
		pass

	def verify(self):
		pass
		

class AuthorizationFailed(Exception):
	"Your given username/password was denied access."
