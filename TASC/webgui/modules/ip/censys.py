import json
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def censys_ip(IP):
    return {'ip': '52.187.23.157', 'autonomous_system': {'description': 'MICROSOFT-CORP-MSN-AS-BLOCK, US', 'routed_prefix': '52.160.0.0/11', 'country_code': 'US', 'organization': 'US', 'asn': 8075, 'name': 'MICROSOFT-CORP-MSN-AS-BLOCK,'}, 'location': [{'city': 'Singapore', 'country': 'Singapore', 'time_zone': 'Asia/Singapore', 'longitude': 103.8547, 'is_anonymous_proxy': False, 'postal_code': '18', 'country_code': 'SG', 'latitude': 1.2929, 'continent': 'Asia', 'is_satellite_provider': False}]}
    url = "https://censys.io/ipv4/"+IP+"/raw"
    try:
        response=requests.get(url,verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')
        soup=soup.find(attrs={"class":"json"})
        return json.loads(soup.text)
    except:
        return {'Error':'Unavailable'}

def censysapi(IP):
    API_URL = "https://censys.io/api/v1"
    UID = "1f6ff94b-49c4-4152-bfee-f948c3824387"
    SECRET = "xPxBsdlgEEL44QLPgivkIiz0TGDhatfP"
    
    res = requests.get(API_URL + "/search/ipv4",data={"80.http.get.headers.server": "Apache"},auth=(UID, SECRET))
    try:
        if res.status_code != 200:
            return {'Error':res.json()["error"]}
        else:
            for name, series in res.json()["raw_series"].items():
                print(series["name"], "was last updated at", series["latest_result"]["timestamp"])
            return res.json()["raw_series"]
    except:
        return {'Error':"Something Went Wrong"}