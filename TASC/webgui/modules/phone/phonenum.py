
import requests
from .act import ACT

def HLRlookup(phonenum, hrlapi):

    api_key = hrlapi
    url1 = ("http://apilayer.net/api/validate?access_key="+api_key+"&number="+phonenum)
    resp = requests.get(url1)
    details = resp.json()
 
    # PWD = "uTb5-CYC%-WTqm-MBaY-!aAT-ApSq"
    # devansh76-api-3874a453262b

    Full_url = 'https://www.hlr-lookups.com/api?action=submitSyncLookupRequest&msisdn=' + phonenum + '&username=devansh76-api-3874a453262b&password=uTb5-CYC%-WTqm-MBaY-!aAT-ApSq'

    response = requests.get(url=Full_url)

    dict = response.json()
    
    results = dict['results']
    
    hlrdata = results[0]

    if details['location'] != '':
        
        location = details['location']

        loc = {'location':location}

        hlrdata.update(loc)

    # ACT data

    actresult = ACT(phonenum)

    if actresult != '':
        hlrdata.update(actresult)

    else:
        pass

    return hlrdata

