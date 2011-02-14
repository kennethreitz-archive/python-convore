# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from datetime import datetime

class ConvoreMessages(object):
    def __init__(self, client, topic_id):
        self.client = client
        self.topic_id = topic_id

    def __call__(self):
        response = self.client._make_request(command="topics/%s/messages.json" % self.topic_id)
        messages = []
        for m in response['messages']:
            message = ConvoreMessage(m)
            messages.append(message)
        return messages
            
    def create(self, message):
        params = {
            'message': message,
            'topic_id': self.topic_id
            }
        response = self.client._make_request(command="topics/%s/messages/create.json" % self.topic_id,
                                             params=params)
        return ConvoreMessage(response['message'])

class ConvoreMessage(object):
    def __init__(self, m):
        self.date_created  = datetime.utcfromtimestamp(m['date_created'])
        self.message       = m['message']
        self.user          = ConvoreUser(m['user'])
        self.id            = m['id']
        
    def __str__(self):
        return "<ConvoreMessage id='%s'>" % self.id

    def __repr__(self):
        return "<ConvoreMessage " + ",".join(map(str,(
                    self.date_created,
                    self.message,
                    self.user,
                    self.id,
                    ))) + ">"
