# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from topic import ConvoreTopics
from datetime import datetime

class ConvoreGroups(object):
    def __init__(self, client):
        self.client = client

    def __call__(self):
        response = self.client._make_request(command="groups.json")
        groups = []
        for g in response['groups']:
            group = ConvoreGroup(g, self.client)
            groups.append(group)
        return groups

    def __getitem__(self, group_id):
        response = self.client._make_request(command="groups/%s.json" % group_id)
        return ConvoreGroup(response['group'], self.client)

    def create(self, name, description=None, slug=None):
        params = {'name': name}
        if description:
            params['description'] = description
        if slug:
            params['slug'] = slug
        print params
        response = self.client._make_request(command="groups/create.json",
                                             params=params)
        return ConvoreGroup(g, self.client)


class ConvoreGroup(object):
    def __init__(self, g, client):
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

        self.client = client
        self.topics = ConvoreTopics(self.client, self.id)

    def leave(self):
        params = {'group_id': self.id}
        response = self.client._make_request(command="groups/%s/leave.json" % self.id, 
                                             params=params)
        print response

    def __str__(self):
        return "<ConvoreGroup id='%s'>" % self.id

    def __repr__(self):
        return "<ConvoreGroup " + ",".join(map(str,(
                    self.members_count,
                    self.name,
                    self.creator,
                    self.url,
                    self.slug,
                    self.date_latest_message,
                    self.date_created,
                    self.topics_count,
                    self.unread,
                    self.id,
                    ))) + ">"

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

    group = ConvoreGroup(g, None)
    print group
    print repr(group)
