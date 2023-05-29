import base64
from django import template

register = template.Library()

@register.filter
def b64encode(string):
    return base64.b64encode(string).decode('utf-8')
