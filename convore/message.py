# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from datetime import datetime

class ConvoreMessage(object):
    def __init__(self, m):
        self.date_created  = datetime.utcfromtimestamp(m['date_created'])
        self.message       = m['message']
        self.user          = ConvoreUser(m['user'])
        self.id            = m['id']
        
    def __str__(self):
        return ",".join(map(str,(
                    self.date_created,
                    self.message,
                    "(%s)" % self.user,
                    self.id,
                    )))
