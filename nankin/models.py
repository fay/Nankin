# -*- coding: utf-8 -*-
from google.appengine.ext import db
from appengine_django.auth.models import User
class Comment(db.Model):
    what = db.TextProperty()
    who = db.ReferenceProperty(User)
    when = db.DateTimeProperty(auto_now_add=True)
    refer = db.ReferenceProperty(db.Model)
    def create(self):
        self.refer.comment_num += 1
        self.refer.put()
        self.put()
    
    def remove(self):
        self.refer.comment_num -= 1
        self.refer.put()
        self.delete()
        
class Jot(db.Model):
    id = db.IntegerProperty()
    title = db.StringProperty()
    what = db.TextProperty()
    when = db.DateTimeProperty(auto_now_add=True)
    #提交者
    #who = db.UserProperty()
    who = db.ReferenceProperty(User)
    type = db.StringProperty()
    tags = db.StringListProperty()
    #评论数
    comment_num = db.IntegerProperty(default=0)
    #阅读次数
    read_num = db.IntegerProperty(default=0)
    like = db.IntegerProperty(default=0)
    unlike = db.IntegerProperty(default=0)
    
    def create(self):
        #每添加一个记录，id值自增。
        max_id = Jot.all().order("-id").get()
        if max_id:
            self.id = (max_id.id or 0) + 1
        else:
            self.id = 1
        self.put()
    
    def remove(self):
        comments = Comment.all().filter("refer = ", self)
        for comment in comments:
            comment.delete()
        self.delete()
        
class Vote(db.Model):
    jot = db.ReferenceProperty(Jot)
    who = db.UserProperty()
    

class Meta(db.Model):
    max_like = db.IntegerProperty(default=0)
    max_unlike = db.IntegerProperty(default=0)
    
    @classmethod
    def get(cls):
        meta = cls.all().get()
        if not meta:
            meta = Meta()
        return meta