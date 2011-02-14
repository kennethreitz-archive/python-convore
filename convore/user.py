# -*- coding: utf-8 -*-
"""
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
"""

from datetime import datetime

class ConvoreUser(object):
    def __init__(self, u):
        self.username = u['username']
        self.url      = u['url']
        self.id       = u['id']
        self.img      = u['img']

    def __str__ (self):
        return ",".join(map(str,(
                    self.username,
                    self.url,
                    self.id,
                    self.img)))
