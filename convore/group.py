# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from datetime import datetime

class ConvoreGroup(object):
    def __init__(self, g):
        self.members_count = g['members_count']
        self.name          = g['name']
        self.creator       = ConvoreUser(g['creator'])
        self.url           = g['url']
        self.slug          = g['slug']
        self.date_latest_message = datetime.utcfromtimestamp(g['date_latest_message'])
        self.date_created        = datetime.utcfromtimestamp(g['date_created'])
        self.topics_count  = g['topics_count'] if 'topics_count' in g else None
        self.unread        = g['unread'] if 'unread' in g else None
        self.id            = g['id']

    def __str__(self):
        return ",".join(map(str,(
                    self.members_count,
                    self.name,
                    "(%s)" % self.creator,
                    self.url,
                    self.slug,
                    self.date_latest_message,
                    self.date_created,
                    self.topics_count,
                    self.unread,
                    self.id,
                    )))

if __name__ == "__main__":
    g = {"date_latest_message": 1297661354.6135991, 
         "topics_count": 16, 
         "members_count": 643, 
         "name": "Python", 
         "creator": {"username": "fdrake", 
                     "url": "/users/fdrake/", 
                     "id": "886", 
                     "img": "https://convore2.s3.amazonaws.com/userpics/886/1297277206.jpg"}, 
         "url": "/python/", 
         "date_created": 1297306311.4270909, 
         "unread": 0, 
         "id": "292", 
         "slug": "python"
         }

    group = ConvoreGroup(g)
    print group
