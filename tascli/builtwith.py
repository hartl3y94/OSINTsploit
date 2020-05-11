#bbf59299-a883-4c08-90a3-c8bec58ebeb9
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pprint

def builtwith(domain,api_key):
    
    url="https://api.builtwith.com/free1/api.json?KEY="+api_key+"&LOOKUP="+domain
    response=requests.get(url,verify=False)
    data=response.json()['groups']
    output={}
    for i in data:
        if 'categories' in i.keys():
            temp=[]
            for j in i['categories']:
                temp.append(j['name'])
        if len(temp)>0:
            output[str(i['name'])]=temp
    return output
print(builtwith("secarmy.org","bbf59299-a883-4c08-90a3-c8bec58ebeb9"))
