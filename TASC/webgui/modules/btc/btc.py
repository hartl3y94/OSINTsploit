import requests
import json 
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def btcaddress(address):
    url="https://rest.bitcoin.com/v2/address/details/"+address
    response = requests.get(url,verify=False)
    data=response.text
    return json.loads(data)