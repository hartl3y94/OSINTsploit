#nR9WHc4ylh6muKnyvau3j8uiSLHF3PgHagIqMXUr
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pprint
import random
from torrequest import TorRequest

def wappalyzer(domain):
    if 1==1:
        headers={
        'Host': 'api.wappalyzer.com',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'x-api-key': 'wappalyzer.api.demo.key',
        #'x-api-key':'nR9WHc4ylh6muKnyvau3j8uiSLHF3PgHagIqMXUr',
        }

        '''ip_addresses=["85.237.57.198:44959", "116.0.2.94:43379", "186.86.247.169:39168", "185.132.179.112:1080", "190.61.44.86:9991"]

        proxy_index = random.randint(0, len(ip_addresses) - 1)
        proxies = {"http": ip_addresses[proxy_index], "https": ip_addresses[proxy_index]}
        '''
        tr=TorRequest(password='16:43AC6502546D255360A3A09D4DAADE253A1244D533070B98B643226C5F')
        tr.reset_identity()

        url="https://api.wappalyzer.com/lookup/v1/?url="+domain
        response=tr.get(url,headers=headers,verify=False)
        data=response.json()
        print(data)
        for i in data:
            for j in i['applications']:
                print("Name:",j['name'])
                if len(j['versions'])!=0:
                    print("Version:",j['versions'])
            print()
        exit()
    #pprint.pprint()

wappalyzer("https://example.com")
