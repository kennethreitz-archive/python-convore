# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from datetime import datetime

class ConvoreTopic(object):
    def __init__(self, t):
        self.name          = t['name']
        self.creator       = ConvoreUser(t['creator'])
        self.url           = t['url']
        self.slug          = t['slug']
        self.date_latest_message = datetime.utcfromtimestamp(t['date_latest_message'])
        self.date_created        = datetime.utcfromtimestamp(t['date_created'])
        self.message_count = t['message_count'] if 'message_count' in t else None
        self.unread        = t['unread'] if 'unread' in t else None
        self.id            = t['id']

    def __str__(self):
        return ",".join(map(str,(
                    self.name,
                    "(%s)" % self.creator,
                    self.url,
                    self.slug,
                    self.date_latest_message,
                    self.date_created,
                    self.message_count,
                    self.unread,
                    self.id,
                    )))
