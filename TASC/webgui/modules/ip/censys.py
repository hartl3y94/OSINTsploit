import json
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def Censys_ip(IP):
    url = "https://censys.io/ipv4/"+IP+"/raw"
    try:
        response=requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup=soup.find(attrs={"class":"json"})
        return json.loads(soup.text)
    except:
        return None