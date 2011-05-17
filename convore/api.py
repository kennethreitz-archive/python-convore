# -*- coding: utf-8 -*-
"""
    convore.api
    ~~~~~~~~~~~

    This module implements the Convore API wrapper objects.

    :copyright: (c) 2011 by Kenneth Reitz.
    :license: ISC, see LICENSE for more details.
"""

import requests

from convore.packages.anyjson import deserialize


API_URL = 'https://convore.com/api/'

# ==========
# Exceptions
# ==========

class LoginFailed(RuntimeError):
    """Login falied!"""

class APIError(RuntimeError):
    """There was a problem properly accessing the Convore API."""

# ==========
# End Points
# ==========

class Call(object):
    def __init__(self, id, url, method, params=[]):
        self.id = id
        self._url = url
        self.method = method
        self.params = params

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id <> other.id

    def clean_params(self, params):
        clean_params = {}
        for p in self.params:
            if p.in_url == False and params.has_key(p.name):
                clean_params[p.name] = params[p.name]
        return clean_params

    def url_params(self, params):
        url_params = {}
        for p in self.params:
            if p.in_url == True and p.name:
                url_params[p.name] = params[p.name]
        return url_params

    def url(self, params):
        url_params = self.url_params(params)
        return ''.join( (API_URL, self._url, '.json')) %(url_params)

    def call(self, auth=None, **params):
        if self.method == 'GET':
            response = self._get(auth, **params)
        elif self.method == 'POST':
            response = self._post(auth, **params)
        else:
            raise APIError('Invalid method %s' %(self.method))

        response.raise_for_status()
        if response.status_code == 401:
            raise InvalidLogin('Invalid login')

        return deserialize(response.content)

    def _get(self, auth=None, **params):
        return requests.get(self.url(params), self.clean_params(params), auth=auth)

    def _post(self, auth=None, **params):
        return requests.post(self.url(params), self.clean_params(params), auth=auth)

class Param(object):
    def __init__(self, name, required, in_url):
        self.name = name
        self.required = required
        self.in_url = in_url

class Endpoints(object):

    """account/verify.json
    Use this method to check if the user is properly logged in.
    https://convore.com/api/account/verify.json
    Request method: GET
    Auth: HTTP basic authentication"""
    account_verify = Call('account_verify', 'account/verify', 'GET')

    """account/mark_read.json
    Mark all messages as read.
    https://convore.com/api/account/mark_read.json
    Request method: POST
    Auth: HTTP basic authentication"""
    account_mark_read = Call('account_mark_read', 'account/mark_read', 'POST')

    """account/online.json
    Get members online now.
    https://convore.com/api/account/online.json
    Request method: GET
    Auth: HTTP basic authentication"""
    account_online = Call('account_online', 'account/online', 'GET')

    """account/mentions.json
    Get the user's mentions.
    https://convore.com/api/account/mentions.json
    Request method: GET
    Auth: HTTP basic authentication"""
    account_mentions = Call('account_mentions', 'account/mentions', 'GET')

    """groups.json
    Get a list of the current user's groups.
    https://convore.com/api/groups.json
    Request method: GET
    Auth: HTTP basic authentication"""
    groups = Call('groups', 'groups', 'GET')

    """groups/create.json
    Create a new group.
    https://convore.com/api/groups/create.json
    The required parameter kind in this request must be a string of either
    public, to represent a group that will be open to the public, or
    private to represent a group whose contents are visible only to its members.
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: name kind
    Optional Parameters: description, slug"""
    group_create = Call('groups_create', 'groups/create', 'POST',
                        [Param('name', True, False),
                         Param('kind', True, False),
                         Param('description', False, False),
                         Param('slug', False, False), ])

    """groups/:group_id.json
    Get detailed information about the group.
    https://convore.com/api/groups/:group_id.json
    Request method: GET
    Required parameters: group_id"""
    group_detail = Call('group_detail', 'groups/%(group_id)s', 'GET',
                        [Param('group_id', True, True),])

    """groups/:group_id/members.json
    Get the group members.
    Note: Specify admin for the optional filter parameter to get only group admins.
    https://convore.com/api/groups/:group_id/members.json
    Request method: GET
    Required parameters: group_id
    Optional parameters: filter"""
    group_members = Call('group_members', 'groups/%(group_id)s/members', 'GET',
                         [Param('group_id', True, True),
                          Param('filter', False, False),])

    """groups/:group_id/join
    Joins a public group.
    https://convore.com/api/groups/:group_id/join.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: group_id"""
    group_join = Call('group_join', 'groups/%(group_id)s/join', 'POST',
                      [Param('group_id', True, True),])

    """groups/:group_id/request.json
    Requests to join a private group.
    https://convore.com/api/groups/:group_id/request.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: group_id"""
    group_request = Call('group_request', 'groups/%(group_id)s/request',
                         'POST', [Param('group_id', True, True),])

    """groups/:group_id/leave.json
    Leave a group.
    https://convore.com/api/groups/:group_id/leave.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: group_id"""
    group_leave = Call('group_leave', 'groups/%(group_id)s/leave', 'POST',
                      [Param('group_id', True, True),])

    """groups/:group_id/online.json
    Get group members online now.
    https://convore.com/api/groups/:group_id/online.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: group_id"""
    group_online = Call('group_online', 'groups/%(group_id)s/online', 'GET',
                      [Param('group_id', True, True),])

    """groups/:group_id/topics.json
    Get the latest topics in a group. Use the optional until_id parameter to
    paginate and get prior topics.
    https://convore.com/api/groups/:group_id/topics.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: group_id
    Optional parameters: until_id"""
    group_topics = Call('group_topics', 'groups/%(group_id)s/topics', 'GET',
                      [Param('group_id', True, True),
                       Param('until_id', False, False),])

    """groups/:group_id/topics/create.json
    Create a new topic.
    https://convore.com/api/groups/:group_id/topics/create.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: group_id, name"""
    group_topic_create = Call('group_topic_create',
                              'groups/%(group_id)s/topics/create', 'POST',
                              [Param('group_id', True, True),
                               Param('name', True, False),])

    """groups/:group_id/mark_read.json
    Mark all messages in the group as read.
    https://convore.com/api/groups/:group_id/mark_read.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: group_id"""
    group_mark_read = Call('group_mark_read', 'groups/%(group_id)s/mark_read',
                           'POST', [Param('group_id', True, True),])

    """topics/:topic_id.json
    Get detailed information about the topic.
    https://convore.com/api/topics/:topic_id.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: topic_id"""
    topic_detail = Call('topic_detail', 'topics/%(topic_id)s', 'GET',
                      [Param('topic_id', True, True),])

    """topics/:topic_id/delete.json
    Delete a topic. You must be the creator of the topic or a group admin in
    order to delete the topic.
    https://convore.com/api/topics/:topic_id/delete.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: topic_id"""
    topic_delete = Call('topic_delete', 'topics/%(topic_id)s/delete', 'POST',
                      [Param('topic_id', True, True),])

    """topics/:topic_id/edit.json
    Edit a topic. You must be the creator of the topic or a group admin in
    order to edit the topic.
    https://convore.com/api/topics/:topic_id/edit.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: topic_id, name"""
    topic_edit = Call('topic_edit', 'topics/%(topic_id)s/edit', 'POST',
                      [Param('topic_id', True, True),
                       Param('name', True, False),])

    """topics/:topic_id/mark_read.json
    Mark all messages in a topic as read.
    https://convore.com/api/topics/:topic_id/mark_read.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: topic_id"""
    topic_mark_read = Call('topic_mark_read', 'topics/%(topic_id)s/mark_read',
                           'POST', [Param('topic_id', True, True),])

    """topics/:topic_id/messages.json
    Get the latest messages in a topic. Use the optional until_id parameter to
    paginate and get prior messages. Set the optional mark_read parameter to
    false to leave the messages as unread.
    https://convore.com/api/topics/:topic_id/messages.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: topic_id
    Optional parameters: until_id, mark_read"""
    topic_messages = Call('topic_messages', 'topics/%(topic_id)s/messages',
                          'GET', [Param('topic_id', True, True),
                                  Param('until_id', False, False),
                                  Param('mark_read', False, False),])

    """topics/:topic_id/messages/create.json
    Post a new message. Set the optional pasted parameter to true to indicate
    the message should be preformatted.
    https://convore.com/api/topics/:topic_id/messages/create.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: topic_id, message
    Optional parameters: pasted"""
    topic_message_create = Call('topic_message_create',
                                'topics/%(topic_id)s/messages/create', 'POST',
                                [Param('topic_id', True, True),
                                 Param('message', True, False),
                                 Param('pasted', False, False),])

    """messages/:message_id/star.json
    Star a message. If the message has already been starred by this user,
    this endpoint will then unstar the message.
    https://convore.com/api/messages/:message_id/star.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: message_id"""
    message_star = Call('message_star', 'messages/%(message_id)s/star', 'POST',
                      [Param('message_id', True, True),])

    """messages/:message_id/delete.json
    Delete a message. You must be the creator of the message or a
    group admin in order to delete the message.
    https://convore.com/api/messages/:message_id/delete.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: message_id"""
    message_delete = Call('message_delete', 'messages/%(message_id)s/delete',
                          'POST', [Param('message_id', True, True),])

    """users/:user_id.json
    Get detailed information about the user based on their user ID.
    https://convore.com/api/users/:user_id.json
    Request method: GET
    Required parameters: user_id"""
    user_detail_by_id = Call('user_detail_by_id', 'users/%(user_id)s', 'GET',
                      [Param('user_id', True, True),])

    """users/username/:username.json
    Get detailed information about the user based on their username.
    https://convore.com/api/users/username/:username.json
    Request method: GET
    Required parameters: username"""
    user_detail_by_name = Call('user_detail_by_name',
                               'users/username/%(username)s', 'GET',
                               [Param('username', True, True),])

    """messages.json
    Gets a list of direct message conversations for the current user.
    Use the optional until_id parameter to paginate and get prior conversations.
    https://convore.com/api/messages.json
    Request method: GET"""
    direct_messages = Call('direct_messages', 'messages', 'GET')

    """messages/:user_id.json
    Lists the messages between logged-in user and the specified user.
    Use the optional until_id parameter to paginate and get prior messages.
    https://convore.com/api/messages/:user_id.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: user_id"""
    direct_messages_from_user = Call('direct_messages_from_user',
                                     'messages/%(user_id)s', 'GET',
                                     [Param('user_id', True, True),])

    """messages/:user_id/create.json
    Creates a new private message.
    https://convore.com/api/messages/:user_id/create.json
    Request method: POST
    Auth: HTTP basic authentication
    Required parameters: user_id message"""
    direct_message_create = Call('direct_message_create',
                                 'messages/%(user_id)s/create', 'POST',
                                 [Param('user_id', True, True),
                                  Param('message', True, False),])

    """messages/message/:message_id/delete.json
    Deletes a private message that the logged-in user has created.
    https://convore.com/api/messages/message/:message_id/delete.json
    Request method: POST
    Auth: HTTP basic authentication"""
    direct_message_delete = Call( 'direct_message_delete',
                                  'messages/message/%(message_id)s/delete',
                                  'POST', [Param('message_id', True, True),])

    #Group Discovery APIs

    """groups/discover/friend.json
    Gets a list of all of the groups the authenticated user is a member of.
    https://convore.com/api/groups/discover/friend.json
    Request method: GET
    Auth: HTTP basic authentication"""
    discover_groups_by_friend = Call('discover_groups_by_friend',
                                      'groups/discover/friend', 'GET')

    """groups/discover/category.json
    Gets a list of group categories.
    https://convore.com/api/groups/discover/category.json
    Request method: GET
    Auth: HTTP basic authentication"""
    discover_categories = Call('discover_groups_category',
                               'groups/discover/category', 'GET')

    """groups/discover/category/:category_slug.json
    Gets a list of groups in the given category.
    https://convore.com/api/groups/discover/category/:category_slug.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: category_slug"""
    discover_groups_by_category = Call('discover_groups_category',
                                       'groups/discover/category/%(category_slug)s', 'GET',
                                       [Param('category_slug', True, True),])

    """groups/discover/search.json
    Gets a list of groups matching the given search.
    Note: The required q parameter should be the term to be searched for.
    https://convore.com/api/groups/discover/search.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: q"""
    discover_groups_by_search = Call('discover_groups_search',
                                     'groups/discover/search', 'GET',
                                       [Param('q', True, False),])

    """groups/discover/explore/:sort.json
    Gets a list of all groups, sorted either by popularity, recency, or
    alphabetically.
    Note: The required sort parameter should be set to one of popular,
    recent, or alphabetical.
    https://convore.com/api/groups/discover/explore/:sort.json
    Request method: GET
    Auth: HTTP basic authentication
    Required parameters: sort"""
    discover_groups_explore = Call('discover_groups_explore',
                                   'groups/discover/explore/%(sort)s', 'GET',
                                       [Param('sort', True, True),])

    """groups/discover/trending.json
    Gets a list of groups that have very recent activity.
    https://convore.com/api/groups/discover/trending.json
    Request method: GET
    Auth: HTTP basic authentication"""
    discover_groups_trending = Call('discover_groups_trending',
                                    'groups/discover/trending', 'GET')

    #Live API
    """Get real-time updates on Convore via long polling. A request to Live
    can hang for up to 30 seconds so be prepared to wait. The response will
    return sooner if there are new updates.
    If you make an authenticated request you will get all the real-time updates
    for the logged-in user for all their groups. Updates include new message
    notifications, new topic notifications, message deletion notifications,
    member log in and log out notifications, etc. This is super handy for
    making a chat bot.
    Presence is also managed by the Live endpoint. Each request to Live will
    keep the authenticated user present on the site. For this reason, as soon
    as you receive a response from this endpoint, you should start a new request.
    Use the cursor request parameter to track your place and prevent missing
    messages between requests. Each response will contain an _id which you
    should use as the next request's cursor. This will allow you to catch any
    messages you might have missed. The first time you make a request to Live
    you do not need to specify a cursor, or you can optionally set it to null.
    You can optionally specify a topic_id if you're interested in a particular
    topic. However, this parameter doesn't actually do anything yet.
    To get anonymous updates for a particular group, you do not need to be
    authenticated, but you must specify a group_id.
    Use the immediate request parameter to have results returned immediately,
    which will be an error if a cursor is supplied and there are no new messages.
    The frequency at which you will receive updates is passed back as the
    X-Live-Frequency HTTP header, which is set to 30 seconds.
    Note that if you submit an unknown cursor (either it's improperly
    formatted, or it's too old) then we will return an error letting you know
    that no messages could be found. This is usually an indication that too
    much time has passed in-between polls. For example, if a user shuts
    their laptop lid, and then when they re-open it a day later, that cursor
    will be too old and we will return an error.
    live.json
    Get live updates about activity on the site.
    https://convore.com/api/live.json
    Request method: GET
    Auth: HTTP basic authentication or none
    Required parameters: group_id (if unauthenticated)
    Optional Parameters: cursor, topic_id, immediate"""
    live = Call('live', 'live', 'GET', [Param('group_id', False, False),
                                        Param('cursor', False, False),
                                        Param('topic_id', False, False),
                                        Param('immediate', False, False),])


    def __init__(self, auth):
        super(Endpoints, self).__init__()
        self.auth = auth

    def call(self, endpoint, **params):
        return endpoint.call(auth=self.auth, **params)

