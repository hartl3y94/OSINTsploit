
import requests
from .act import ACT

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