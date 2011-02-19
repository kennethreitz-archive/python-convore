class User(object):
    """Convore User object."""

    def __init__(self):
        self.username = None
        self.url = None
        self.id = None
        self.img = None

    def import_from_api(self, dict):
        self.username = dict['username']
        self.url = dict['url']
        self.id = dict['id']
        self.img = dict['img']

    def __repr__(self):
        return '<user @%s>' % (self.username)

class Group(object):
    """Convore Group object."""
    
    def __init__(self):
        self.kind = None
        self.members_count = None
        self.name = None
        self.creator = None
        self.url = None
        self.slug = None
        self.date_latest_message = None
        self.date_created = None
        self.topics_count = None
        self.unread = None
        self.id = None

    def import_from_api(self, dict):
        self.kind = dict['kind']
        self.members_count = dict['members_count']
        self.name = dict['name']
        self.creator = User()
        self.creator.import_from_api(dict['creator'])
        self.url = dict['url']
        self.slug = dict['slug']
        self.date_latest_message = dict['date_latest_message']
        self.date_created = dict['date_created']
        # self.topics_count = dict['topics_count']
        # self.unread = dict['unread']
        self.id = dict['id']

    def __repr__(self):
        return '<group %s>' % (self.slug)
