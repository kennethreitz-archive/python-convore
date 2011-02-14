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

    def __str__(self):
        return "<ConvoreUser id='%s'>" % self.id

    def __repr__ (self):
        return ",".join(map(str,(
                    self.username,
                    self.url,
                    self.id,
                    self.img)))

if __name__ == "__main__":
    u = {"username": "ksato9700", 
         "url": "/users/ksato9700/",
         "id": 8849, 
         "img": "https://convore2.s3.amazonaws.com/userpics/8849/1297620465.jpg"}

    user = ConvoreUser(u)
    print user
    print repr(user)
