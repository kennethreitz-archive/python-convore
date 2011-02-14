# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from message import ConvoreMessages
from datetime import datetime

class ConvoreTopics(object):
    def __init__(self, client, group_id=None):
        self.client = client
        self.group_id = group_id

    def __call__(self):
        response = self.client._make_request(command="groups/%s/topics.json" % self.group_id)
        topics = []
        for t in response['topics']:
            topic = ConvoreTopic(t, self.client)
            topics.append(topic)
        return topics

    def __getitem__(self, topic_id):
        response = self.client._make_request(command="topics/%s.json" % topic_id)
        return ConvoreTopic(response['topic'], self.client)

    def create(self, name):
        if self.group_id == None:
            raise RuntimeError("topics should be created with group_id")
            
        params = {
            'name': name,
            'group_id': self.group_id
            }
        response = self.client._make_request(command="groups/%s/topics/create.json" % self.group_id,
                                             params=params)
        return ConvoreTopic(response['topic'], self.client)

class ConvoreTopic(object):
    def __init__(self, t, client):
        self.name          = t['name']
        self.creator       = ConvoreUser(t['creator'])
        self.url           = t['url']
        self.slug          = t['slug']
        self.date_latest_message = datetime.utcfromtimestamp(t['date_latest_message'])
        self.date_created        = datetime.utcfromtimestamp(t['date_created'])
        self.message_count = t['message_count'] if 'message_count' in t else None
        self.unread        = t['unread'] if 'unread' in t else None
        self.id            = t['id']

        self.client = client
        self.messages = ConvoreMessages(self.client, self.id)

    def __str__(self):
        return "<ConvoreTopic id='%s'>" % self.id

    def __repr__(self):
        return "<ConvoreTopic " + ",".join(map(str,(
                    self.name,
                    self.creator,
                    self.url,
                    self.slug,
                    self.date_latest_message,
                    self.date_created,
                    self.message_count,
                    self.unread,
                    self.id,
                    ))) + ">"
