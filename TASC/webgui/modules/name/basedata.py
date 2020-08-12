import requests
import json

def getGender(name):

    url = "https://api.genderize.io/?name="+name
    response = requests.get(url).json()
    gender = {}
    if response["gender"] == 'null':
        return None
    gender['gender'] = response['gender']
    gender['probability'] = response['probability']
    return gender

def getNation(name):

    url = "https://api.nationalize.io/?name="+name
    response = requests.get(url).json()
    nation = {}
    if response['country'] == []:
        return None
    country_id = response['country'][0]['country_id']
    country_name = requests.get("https://restcountries.eu/rest/v2/alpha/"+country_id).json()
    nation['country'] = country_name['name']

    nation['probability'] = response['country'][0]['probability']
    return nation

def getBasedata(name):
    
    basedata = {}
    gender = getGender(name)
    if not gender['gender'] == None:
        basedata['gender'] = gender
    nation = getNation(name)
    if not nation == None:
        basedata['nation'] = nation
    
    return basedata

#getBasedata("Harshavarthnan")