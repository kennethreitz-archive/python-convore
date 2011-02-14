# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

import urllib2
import json

from group import ConvoreGroup
from topic import ConvoreTopic
from message import ConvoreMessage
from live import ConvoreLiveMessage

URL_PREFIX = "https://convore.com/api/"
debug=0

class ConvoreError(Exception):
	pass

class ConvoreAuthError(ConvoreError):
	pass

class ConvoreClient(object):

	def __init__(self, username, password):
		auth_handler = urllib2.HTTPBasicAuthHandler()
		auth_handler.add_password(realm='Convore',
					  uri=URL_PREFIX,
					  user=username,
					  passwd=password)
		self.openr = urllib2.build_opener(auth_handler,
						  urllib2.HTTPCookieProcessor(),
						  urllib2.HTTPSHandler(debug))

	def _make_request(self, command, data=None, headers={}):
		url = URL_PREFIX + command
		try:
			return self.openr.open(urllib2.Request(url = URL_PREFIX + command, 
							       data=data,
							       headers=headers))
		except urllib2.HTTPError as e:
			if e.code == 401:
				raise ConvoreAuthError() 
			else:
				raise

	def verify(self):
		self._make_request(command="account/verify.json")
		
	def groups(self):
		response = self._make_request(command="groups.json")
		groups = []
		for g in json.load(response)['groups']:
			groups.append(ConvoreGroup(g))
		return groups
		
	def group_by_id(self, group_id):
		response = self._make_request(command="groups/%s.json" % group_id)
		return ConvoreGroup(json.load(response)['group'])

	def topics(self, group):
		response = self._make_request(command="groups/%s/topics.json" % group.id)
		topics = []
		for t in json.load(response)['topics']:
			topics.append(ConvoreTopic(t))
		return topics

	def topic_by_id(self, topic_id):
		response = self._make_request(command="topics/%s.json" % topic_id)
		return ConvoreTopic(json.load(response)['topic'])

	def live(self, group_id=None, cursor=None, topic_id=None):
		data = {}
		if group_id:
			data['group_id'] = group_id
		if cursor:
			data['cursor'] = cursor
		if topic_id:
			data['topic_id'] = topic_id
		response = self._make_request(command="live")
		messages = []
		for m in json.load(response)['messages']:
			messages.append(ConvoreLiveMessage(m))
		return messages


	def messages(self, topic):
		response = self._make_request(command="topics/%s/messages.json" % topic.id)
		messages = []
		for m in json.load(response)['messages']:
			print m
			messages.append(ConvoreMessage(m))
		return messages

if __name__ == '__main__':
	import sys
	username, password = sys.argv[1:3]
	client = ConvoreClient(username, password)
	#client.verify()

	for group in client.groups():
		print group
		print repr(group)

	#group_id = 3011
	group_id = group.id

	group = client.group_by_id(group_id)
	for topic in client.topics(group):
		print topic
		print repr(topic)
	
	#topic_id = 5068
	topic_id = topic.id

	topic = client.topic_by_id(topic_id)
	for message in client.messages(topic):
		print message
		print repr(message)

	#for message in client.live():
	#	print message
		
