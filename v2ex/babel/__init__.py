SYSTEM_VERSION = '2.4.0-RC1'

import datetime
import hashlib

from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import users

class Member(db.Model):
    num = db.IntegerProperty(indexed=True)
    auth = db.StringProperty(required=False, indexed=True)
    deactivated = db.IntegerProperty(required=True, default=0)
    username = db.StringProperty(required=False, indexed=True)
    username_lower = db.StringProperty(required=False, indexed=True)
    password = db.StringProperty(required=False, indexed=True)
    email = db.StringProperty(required=False, indexed=True)
    email_verified = db.IntegerProperty(required=False, indexed=True, default=0)
    website = db.StringProperty(required=False, default='')
    twitter = db.StringProperty(required=False, default='')
    twitter_oauth = db.IntegerProperty(required=False, default=0)
    twitter_oauth_key = db.StringProperty(required=False)
    twitter_oauth_secret = db.StringProperty(required=False)
    twitter_oauth_string = db.StringProperty(required=False)
    twitter_sync = db.IntegerProperty(required=False, default=0)
    twitter_id = db.IntegerProperty(required=False)
    twitter_name = db.StringProperty(required=False)
    twitter_screen_name = db.StringProperty(required=False)
    twitter_location = db.StringProperty(required=False)
    twitter_description = db.TextProperty(required=False)
    twitter_profile_image_url = db.StringProperty(required=False)
    twitter_url = db.StringProperty(required=False)
    twitter_statuses_count = db.IntegerProperty(required=False)
    twitter_followers_count = db.IntegerProperty(required=False)
    twitter_friends_count = db.IntegerProperty(required=False)
    twitter_favourites_count = db.IntegerProperty(required=False)
    location = db.StringProperty(required=False, default='')
    tagline = db.TextProperty(required=False, default='')
    bio = db.TextProperty(required=False, default='')
    avatar_large_url = db.StringProperty(required=False, indexed=False)
    avatar_normal_url = db.StringProperty(required=False, indexed=False)
    avatar_mini_url = db.StringProperty(required=False, indexed=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    last_signin = db.DateTimeProperty()
    blocked = db.TextProperty(required=False, default='')
    l10n = db.StringProperty(default='en')
    favorited_nodes = db.IntegerProperty(required=True, default=0)
    favorited_topics = db.IntegerProperty(required=True, default=0)
    favorited_members = db.IntegerProperty(required=True, default=0)
    followers_count = db.IntegerProperty(required=True, default=0)
    
    def hasFavorited(self, something):
        if type(something).__name__ == 'Node':
            n = 'r/n' + str(something.num) + '/m' + str(self.num)
            r = memcache.get(n)
            if r:
                return r
            else:
                q = db.GqlQuery("SELECT * FROM NodeBookmark WHERE node =:1 AND member = :2", something, self)
                if q.count() > 0:
                    memcache.set(n, True, 86400 * 14)
                    return True
                else:
                    memcache.set(n, False, 86400 * 14)
                    return False
        else:
            if type(something).__name__ == 'Topic':
                n = 'r/t' + str(something.num) + '/m' + str(self.num)
                r = memcache.get(n)
                if r:
                    return r
                else:
                    q = db.GqlQuery("SELECT * FROM TopicBookmark WHERE topic =:1 AND member = :2", something, self)
                    if q.count() > 0:
                        memcache.set(n, True, 86400 * 14)
                        return True
                    else:
                        memcache.set(n, False, 86400 * 14)
                        return False
            else:
                if type(something).__name__ == 'Member':
                    n = 'r/m' + str(something.num) + '/m' + str(self.num)
                    r = memcache.get(n)
                    if r:
                        return r
                    else:
                        q = db.GqlQuery("SELECT * FROM MemberBookmark WHERE one =:1 AND member_num = :2", something, self.num)
                        if q.count() > 0:
                            memcache.set(n, True, 86400 * 14)
                            return True
                        else:
                            memcache.set(n, False, 86400 * 14)
                            return False
                else:
                    return False
    
class Counter(db.Model):
    name = db.StringProperty(required=False, indexed=True)
    value = db.IntegerProperty()
    created = db.DateTimeProperty(auto_now_add=True)
    last_increased = db.DateTimeProperty(auto_now=True)
    
#class Section(db.Model):
#    num = db.IntegerProperty(indexed=True)
#    name = db.StringProperty(required=False, indexed=True)
#    title = db.StringProperty(required=False, indexed=True)
#    title_alternative = db.StringProperty(required=False, indexed=True)
#    header = db.TextProperty(required=False)
#    footer = db.TextProperty(required=False)
#    nodes = db.IntegerProperty(default=0)
#    created = db.DateTimeProperty(auto_now_add=True)
#    last_modified = db.DateTimeProperty(auto_now=True)
    
class Node(db.Model):
    num = db.IntegerProperty(indexed=True)
    section_num = db.IntegerProperty(indexed=True)
    name = db.StringProperty(required=False, indexed=True)
    title = db.StringProperty(required=False, indexed=True)
    title_alternative = db.StringProperty(required=False, indexed=True)
    header = db.TextProperty(required=False)
    footer = db.TextProperty(required=False)
    sidebar = db.TextProperty(default='')
    category = db.StringProperty(required=False, indexed=True)
    topics = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    enabled = db.BooleanProperty(default=True)
    
class Topic(db.Model):
    num = db.IntegerProperty(indexed=True)
    node = db.ReferenceProperty(Node)
    node_num = db.IntegerProperty(indexed=True)
    node_name = db.StringProperty(required=False, indexed=True)
    node_title = db.StringProperty(required=False, indexed=False)
    member = db.ReferenceProperty(Member)
    member_num = db.IntegerProperty(indexed=True)
    title = db.StringProperty(required=False, indexed=True)
    content = db.TextProperty(required=False)
    content_rendered = db.TextProperty(required=False)
    content_length = db.IntegerProperty(default=0)
    hits = db.IntegerProperty(default=0)
    stars = db.IntegerProperty(required=True, default=0)
    replies = db.IntegerProperty(default=0)
    created_by = db.StringProperty(required=False, indexed=True)
    last_reply_by = db.StringProperty(required=False, indexed=True)
    source = db.StringProperty(required=False, indexed=True)
    type = db.StringProperty(required=False, indexed=True)
    type_color = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    last_touched = db.DateTimeProperty()
    
class Reply(db.Model):
    num = db.IntegerProperty(indexed=True)
    topic = db.ReferenceProperty(Topic)
    topic_num = db.IntegerProperty(indexed=True)
    member = db.ReferenceProperty(Member)
    member_num = db.IntegerProperty(indexed=True)
    content = db.TextProperty(required=False)
    source = db.StringProperty(required=False, indexed=True)
    created_by = db.StringProperty(required=False, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)
    
class Avatar(db.Model):
    num = db.IntegerProperty(indexed=True)
    name = db.StringProperty(required=False, indexed=True)
    content = db.BlobProperty()
    
class Note(db.Model):
    num = db.IntegerProperty(indexed=True)
    member = db.ReferenceProperty(Member)
    member_num = db.IntegerProperty(indexed=True)
    title = db.StringProperty(required=False, indexed=True)
    content = db.TextProperty(required=False)
    body = db.TextProperty(required=False)
    length = db.IntegerProperty(indexed=False, default=0)
    edits = db.IntegerProperty(indexed=False, default=1)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

class PasswordResetToken(db.Model):
    token = db.StringProperty(required=False, indexed=True)
    email = db.StringProperty(required=False, indexed=True)
    member = db.ReferenceProperty(Member)
    valid = db.IntegerProperty(required=False, indexed=True, default=1)
    timestamp = db.IntegerProperty(required=False, indexed=True, default=0)

class Place(db.Model):
    num = db.IntegerProperty(required=False, indexed=True)
    ip = db.StringProperty(required=False, indexed=True)
    name = db.StringProperty(required=False, indexed=False)
    visitors = db.IntegerProperty(required=False, default=0, indexed=True)
    longitude = db.FloatProperty(required=False, default=0.0, indexed=True)
    latitude = db.FloatProperty(required=False, default=0.0, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

class PlaceMessage(db.Model):
    num = db.IntegerProperty(indexed=True)
    place = db.ReferenceProperty(Place)
    place_num = db.IntegerProperty(indexed=True)
    member = db.ReferenceProperty(Member)
    content = db.TextProperty(required=False)
    in_reply_to = db.SelfReferenceProperty()
    source = db.StringProperty(required=False, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)

class Checkin(db.Model):
    place = db.ReferenceProperty(Place)
    member = db.ReferenceProperty(Member)
    last_checked_in = db.DateTimeProperty(auto_now=True)
    
class Site(db.Model):
    num = db.IntegerProperty(required=False, indexed=True)
    title = db.StringProperty(required=False, indexed=False)
    slogan = db.StringProperty(required=False, indexed=False)
    description = db.TextProperty(required=False)
    domain = db.StringProperty(required=False, indexed=False)
    analytics = db.StringProperty(required=False, indexed=False)
    home_categories = db.TextProperty(required=False, indexed=False)
    l10n = db.StringProperty(default='en')
    use_topic_types = db.BooleanProperty(default=False)
    topic_types = db.TextProperty(default='')
    
class Minisite(db.Model):
    num = db.IntegerProperty(required=False, indexed=True)
    name = db.StringProperty(required=False, indexed=True)
    title = db.StringProperty(required=False, indexed=False)
    description = db.TextProperty(default='')
    pages = db.IntegerProperty(default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

class Page(db.Model):
    num = db.IntegerProperty(required=False, indexed=True)
    name = db.StringProperty(required=False, indexed=True)
    title = db.StringProperty(required=False, indexed=False)
    minisite = db.ReferenceProperty(Minisite)
    content = db.TextProperty(default='')
    content_rendered = db.TextProperty(default='')
    content_type = db.StringProperty(default='text/html')
    weight = db.IntegerProperty(required=True, default=0)
    mode = db.IntegerProperty(required=True, default=0)
    hits = db.IntegerProperty(required=True, default=0)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

class NodeBookmark(db.Model):
    node = db.ReferenceProperty(Node, indexed=True)
    member = db.ReferenceProperty(Member, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)

class TopicBookmark(db.Model):
    topic = db.ReferenceProperty(Topic, indexed=True)
    member = db.ReferenceProperty(Member, indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)

class MemberBookmark(db.Model):
    one = db.ReferenceProperty(Member, indexed=True)
    member_num = db.IntegerProperty(indexed=True)
    created = db.DateTimeProperty(auto_now_add=True)