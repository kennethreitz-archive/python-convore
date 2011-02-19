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
        self.joined = False

    def import_from_api(self, d):
        self.creator = User()

        self.kind = d.get('kind', None)
        self.members_count = d.get('members_count', None)
        self.name = d.get('name', None)
        self.creator.import_from_api(d.get('creator', None))
        self.url = d.get('url', None)
        self.slug = d.get('slug', None)
        self.date_latest_message = d.get('date_latest_message', None)
        self.date_created = d.get('date_created', None)
        self.topics_count = d.get('topics_count', None)
        self.unread = d.get('unread', None)
        self.id = d.get('id', None)
        
    def __repr__(self):
        return '<group %s>' % (self.slug)
