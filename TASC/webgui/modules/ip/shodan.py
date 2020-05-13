import requests
import json

def shodan_ip(IP,apikey):
    shodan={}
    shodan['honeypot']=honeypot(IP,apikey)
    url="https://api.shodan.io/shodan/host/"+IP+"?key="+apikey
    try:
        response=requests.get(url)
        js=json.loads(response.text)
        shodan['host']=js
        return shodan
    except:
        return {'Error':'Something Went Wrong'}
    
def honeypot(ip,apikey):
    result={}
    honey = "https://api.shodan.io/labs/honeyscore/"+ip+"?key="+apikey
    try:
        probability= requests.get(honey).text
        if ("error" in result) or ("404" in result):
            result['Error'] = 'IP Not Found'
        else:
            result['HoneyPot Percentage']=str(float(probability) * 100) 
            return result
    except:
        result['Error']='No Information Found'
    else:
        result['Error']='Something Went Wrong'
    return result