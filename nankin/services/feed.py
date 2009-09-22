# -*- coding:utf-8 -*-
from django.contrib.syndication.feeds import Feed
from nankin.models import Jot
class LatestJot(Feed):
    def item_link(self,item):
        return '/view/'+item.key().__str__()
    def title(self, obj):
        return "新鲜出炉的文章"
    def link(self, obj):
        return "http://nan-kin.appspot.com"
    def description(self, obj):
        return "得瑟啥？趁热看..."
    def item_pubdate(self, item):
        return item.when
    def item_guid(self,item):
        return item.key().__str__()
    def items(self,obj):
        jots = Jot.all().order('-when').fetch(10, 0)
        return jots

