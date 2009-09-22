# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser

PAGE_SIZE = 10

def createPaginator(page,page_size=PAGE_SIZE):
    paginator = ''
    if page != 1:
        paginator += '<a href=\"?page=' + str(page - 1) + '\">‹ Pre</a>  '
    paginator += str((page - 1) * page_size + 1) + '-' + str(page * page_size) + ' '
    paginator += '<a href=\"?page=' + str(page + 1) + '\">Next ›</a>'
    return paginator

def standard_ratio(max_value,min_value,value):
    offset = max_value - min_value
    if offset > 110:
        ratio = offset/110.0
        return value/ratio
    else:
        return value 
    
def strip_tags(html):
    html = html.strip()
    html = html.strip("\n")
    result = []
    parser = HTMLParser()
    parser.handle_data = result.append
    parser.feed(html)
    parser.close()
    return ''.join(result)