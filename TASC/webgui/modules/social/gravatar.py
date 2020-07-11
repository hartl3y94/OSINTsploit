import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json

def gravatar(username):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
    }
    url="https://en.gravatar.com/"+username+".json"
    response=requests.get(url,headers=headers,verify=False)
    #print(response.text)
    try:
      if "User not found" not in response.text:
          return json.loads(response.text)
    except:
        gravatar = {}
        gravatar['Error'] = 'Profile not found'
        return gravatar

#print(gravatar("akinfosec"))