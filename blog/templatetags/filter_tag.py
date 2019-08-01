# -*- coding:utf-8 -*-
"""
自定义过滤器和标签
"""
from html.parser import HTMLParser
from django import template
import random
import re

register = template.Library()


@register.simple_tag
def get_random_color():
    color_list = ['bg-info', 'bg-success', 'bg-warning', 'bg-yellow', '']
    color = random.choice(color_list)
    return color


@register.simple_tag
def keyword_to_red(value='', keyword=''):
    new = value.lower()
    new = new.replace(keyword.lower(), '<span style="color:red">' + keyword.lower() + '</span>')
    ii = re.search(keyword, new)
    if ii:
        start = ii.span()[0]
        if len(new) > 80:
            new = new[start - 24:start + 120]
    else:
        if len(new) > 80:
            new = new[0:60]
    return new


@register.simple_tag
def filter_tag(content):
    content = re.sub('<.*?>', '', content)
    h = HTMLParser()
    content = h.unescape(content)
    return content
