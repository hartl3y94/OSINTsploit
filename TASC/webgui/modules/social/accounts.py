import requests 
import json 
from threading import Thread
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("./webgui/modules/src/web_accounts_list.json") as f:
    weblist = json.loads(f.read())

accounts=[]

def accountcheck(url,website):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Accept-Encoding' : 'gzip, deflate'
          }
    try:
        response = requests.get(url,headers=headers,timeout=60, verify=False, allow_redirects=False)
        if int(response.status_code) == int(website['account_existence_code']) and response.text.find(website["account_existence_string"]) > 0:
            accounts.append(url.split("/")[2])
    except:
        pass

def whatismyname(username):
    threads=[]
    for i in weblist['sites']:
        if i['valid']:
            process = Thread(target=accountcheck,args=[i['check_uri'].format(account=username),i])
            process.start()
            threads.append(process)
    for process in threads:
        process.join()
        
    if len(accounts)>0:
        return accounts
    else:
        return None
