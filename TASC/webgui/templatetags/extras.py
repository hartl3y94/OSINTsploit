import json, yaml

from django import template

register = template.Library()


@register.filter

def pretty_json(value):

    return yaml.dump(value, default_flow_style=False)


@register.filter

def add_query(value):
    value = str(value)
    query = "victimtrack:"
    query = query+value
    return query

@register.filter

def format(value):
    value = str(value)
    value = ','+value
    return value

@register.simple_tag
def define(value):
    value = "victimtrack:"+value
    return value

@register.simple_tag
def defines(value):
    value = ","+value
    return value

