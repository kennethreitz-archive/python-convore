# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

from user import ConvoreUser
from datetime import datetime

class ConvoreLiveMessage(object):
    def __init__(self, m):
        self.kind      = m['kind']
        self.group_ids = m['group_ids']
        self.user      = ConvoreUser(m['user'])
        self._ts       = datetime.utcfromtimestamp(m['_ts'])
        self._id       = m['_id']
        
    def __str__(self):
        return "<ConvoreLiveMessage _id='%s'>" % self._id

    def __repr__(self):
        return ",".join(map(str,(
                    self.kind,
                    self.group_ids,
                    self.user,
                    self._ts,
                    self._id,
                    )))
                    

if __name__ == "__main__":
    m = {"kind": "logout", 
         "group_ids": [292], 
         "user": {"username": "ksato9700", 
                  "url": "/users/ksato9700/",
                  "id": 8849, 
                  "img": "https://convore2.s3.amazonaws.com/userpics/8849/1297620465.jpg"}, 
         "_ts": 1297638926.453522, 
         "_id": "2415aa7c-37c7-11e0-a4f2-4040006c4e80"
         }

    message = ConvoreLiveMessage(m)
    print message
    print repr(message)
