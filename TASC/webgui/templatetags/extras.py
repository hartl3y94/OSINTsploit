import json, yaml
from django.contrib.auth.models import User
from django import template
from ..modules.filehandlers import HistoryData

register = template.Library()


@register.filter

def pretty_json(value):

    return yaml.dump(value, default_flow_style=False)

@register.filter

def getnotification(value):
    username = value
    print(username)
    try:
        history = HistoryData("media/json/history_{}.json".format(username),"r")
    except FileNotFoundError:
        history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())
        
    notifications = history['notifications'][:5]
    return notifications


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

