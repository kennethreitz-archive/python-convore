# -*- coding: utf-8 -*-
'''
Copyringt 2011 Kenichi Sato <ksato9700 AT gmail.com>
'''

import urllib
import urllib2
import json

from group import ConvoreGroups
from topic import ConvoreTopics
from live import ConvoreLiveMessage

URL_PREFIX = "https://convore.com/api/"
#debug=100
debug=0

class ConvoreError(Exception):
	pass

class ConvoreAuthError(Exception):
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

		self.groups = ConvoreGroups(self)
		self.topics = ConvoreTopics(self)

	def _make_request(self, command, params=None):
		url = URL_PREFIX + command
		if params:
			data = urllib.urlencode(params)
		else:
			data = None
		headers = {}
		try:
			f = self.openr.open(urllib2.Request(url = URL_PREFIX + command, 
							    data=data,
							    headers=headers))
			response = json.load(f)
			if 'error' in response:
				raise ConvoreError(response['error'])
			return response
		
		except urllib2.HTTPError as e:
			if e.code == 401:
				raise ConvoreAuthError() 
			else:
				raise

	def verify(self):
		self._make_request(command="account/verify.json")
		

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
		for m in response['messages']:
			messages.append(ConvoreLiveMessage(m))
		return messages


if __name__ == '__main__':
	import sys
	try:
		username, password = sys.argv[1:3]
	except:
		print "usage: python %s username password" % sys.argv[0]
		sys.exit(1)

	client = ConvoreClient(username, password)
	#client.verify()

	groups = client.groups()
	print groups
	
	#group = client.groups.create(name="MyTestGroup", description="desc", slug="the group")
	#print repr(group)

	# for group in groups:
	# 	if "test" in group.slug:
	# 		break

	#print group
	# print repr(group)

	# topic = group.topics.create(name="Topic One")
	# print repr(topic)
	
	# topics = group.topics()
	# print topics

	# topic = client.topics[topics[-1].id]
	# print topic
	# print repr(topic)
	
	# topic.messages.create(message="Wow, I'm the first")
	# topic.messages.create(message="Hmm, I must be the second")

	# messages = topic.messages()
	# print messages

	#for message in client.live():
	#	print message
		
