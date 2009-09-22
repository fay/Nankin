# coding: utf-8
from types import *
from datetime import datetime, timedelta
from django.template.defaultfilters import register
import markdown as md
# 功能： 在模板中使用该filter，将会把输入的时间值以一种人性化的表现方式输出，其规则如下： 如果输入的时间值小于当前时间1分钟，就显示xx秒前；
#           如果输入的时间值小于当前时间1个小时，就显示xx分钟前；
#           如果输入的时间值小于当前时间1天，就显示xx小时前；
#           如果输入的时间值小于当前时间1个月，就显示xx天前；
#           如果输入的时间值小于当前时间1年，就显示xx月前；
#           如果输入的时间值大于等于当前时间1年，直接显示日期；
# 输入： value – 模板变量，必须是合乎格式的时间值
# 返回： 人性化的时间显示字符串
@register.filter(name='human_time')    
def human_time(value):
    if type(value) is StringType:
            value = datetime.strptime(value, "%Y-%m-%d %H:%M")
    now = datetime.now()
    # 计算时间差秒数
    seconds = (now - value).seconds
    # 计算时间差天数
    days = (now - value).days
    if days < 1:    
        if seconds < 60:
            return u"%d秒前" % seconds
        if seconds < 3600:
            return u"%d分钟前" % (seconds / 60)
        if seconds < 86400:
            return u"%d小时前" % (seconds / 3600)
    else:
        # 时区修正
        return value + timedelta(hours= + 8)
    """
    else:
        if days < 30:
            return u"%d天前" % days
        if days < 365:
            return u"约%d月前" % (days/30)
        return value 
    """
@register.filter(name='markdown')    
def markdown(value):
    m = md.Markdown()
    html = m.convert(value)
    return html
@register.filter(name='truncatetext')    
def truncatetext(value):
    return value[:40]+' ...'