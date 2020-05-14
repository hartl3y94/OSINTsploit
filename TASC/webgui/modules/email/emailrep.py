import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def emailrep(email,apikey):
    headers = {
        'Key':apikey,
        'User-Agent':'TASC',
        }
    url="https://emailrep.io/"+email
    response=requests.get(url,headers=headers,verify=False)
    data=response.text
    return json.loads(data)