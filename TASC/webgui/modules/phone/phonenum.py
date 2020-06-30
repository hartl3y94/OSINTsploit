
import requests
from .act import ACT
from requests_html import HTMLSession, HTML
from bs4 import BeautifulSoup
import hashlib
import random


def HLRlookup(phonenum, apilayerphone, hlruname,hlrpwd,):

    try:
    
        # PWD = "uTb5-CYC%-WTqm-MBaY-!aAT-ApSq"
        # devansh76-api-3874a453262b
        # &username=devansh76-api-3874a453262b&password=uTb5-CYC%-WTqm-MBaY-!aAT-ApSq

        hlrurl = 'https://www.hlr-lookups.com/api?action=submitSyncLookupRequest&msisdn=' + phonenum + '&username='+hlruname+'&password='+hlrpwd

        response = requests.get(url=hlrurl)

        dict = response.json()
        
        results = dict['results']
        
        hlrdata = results[0]

        apilayerurl = ("http://apilayer.net/api/validate?access_key="+apilayerphone+"&number="+phonenum)
        resp = requests.get(apilayerurl)
        details = resp.json()

        if details['location'] != '':
            
            hlrdata['location'] = details['location']

            hlrdata['line_type'] = details['line_type']

        # ACT data

        actresult = ACT(phonenum)

        if actresult != '':
            hlrdata.update(actresult)

        else:
            pass

        return hlrdata

    except Exception as e:
      
        hlrdata = {}
        hlrdata['error'] = 'Please check your API Credentials'
        return hlrdata
    
def numverify(number):
    session = HTMLSession()
    user_agent_list = [
        #Chrome
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            #Firefox
            'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]
    session.headers={
        "User-Agent":user_agent_list[random.randint(0,len(user_agent_list)-1)],
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://numverify.com/',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'close'
        }
    session.proxies = {'http':  'socks5h://127.0.0.1:9050','https': 'socks5h://127.0.0.1:9050'}

    response=requests.get("https://numverify.com/")
    soup = BeautifulSoup(response.text,"html.parser")
    secret_key=str(soup.find("input",{"name":"scl_request_secret"})['value'])
    #print(secret_key)

    md5_hash = hashlib.md5()
    md5_hash.update(bytes(number+secret_key,"utf-8"))
    secret_key=md5_hash.hexdigest()

    url="https://numverify.com/php_helper_scripts/phone_api.php?secret_key={}&number={}".format(secret_key,number)

    #print(url)
    session.close()
    data = requests.get(url).json()
    return data