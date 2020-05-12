import requests
import json

def shodan_ip(IP,apikey):
    shodan={}
    url="https://api.shodan.io/shodan/host/"+IP+"?key="+apikey
    try:
        response=requests.get(url)
        js=json.loads(response.text)
        shodan['host']=js
        shodan['honeypot']=honeypot(IP,apikey)
    except:
        return {'Error':'Something Went Wrong'}
    
def honeypot(ip,apikey):
    honey = "https://api.shodan.io/labs/honeyscore/"+ip+"?key="+apikey
    try:
        result = requests.get(honey).json
    except:
        result['Message'] ='No information Found'

    if "error" in result or "404" in result:
        result['Error'] = 'IP Not Found'
    elif result:
        probability = str(float(result) * 10)
        result['HoneyPot Probability']=probability
    else:
        result['Error']='Something Went Wrong'
    return result