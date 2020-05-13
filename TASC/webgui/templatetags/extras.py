import json, yaml

from django import template

register = template.Library()


@register.filter

def pretty_json(value):

    return yaml.dump(value, default_flow_style=False)