import requests
import json

def shodan_ip(IP,apikey):

    shodan={}
    honeypotdata =honeypot(IP,apikey)

    if honeypotdata != None:
        shodan['honeypot'] = honeypotdata

    url="https://api.shodan.io/shodan/host/"+IP+"?key="+apikey
    try:
        response=requests.get(url)
        js=json.loads(response.text)
        shodan['host']=js
        if shodan['host']['error']:
            return {'unknownerror':'Something Went Wrong'}
        return shodan
    except:
        return {'unkownerror':'Something Went Wrong'}
    
def honeypot(ip,apikey):
    result={}
    honey = "https://api.shodan.io/labs/honeyscore/"+ip+"?key="+apikey
    try:
        probability= requests.get(honey).text
        if ("error" in result) or ("404" in result):
            pass
        else:
            result['HoneyPot Percentage']=str(float(probability) * 100) 
            return result
    except:
        return