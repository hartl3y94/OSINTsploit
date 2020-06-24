
import requests


def HLRlookup(phonenum, apilayerphone):

    apilayerphone = apilayerphone
    url1 = ("http://apilayer.net/api/validate?access_key="+apilayerphone+"&number="+phonenum)
    resp = requests.get(url1)
    details = resp.json()
    print(details)

    Full_url = 'https://www.hlr-lookups.com/api?action=submitSyncLookupRequest&msisdn=' + phonenum + '&username=devansh76-api-3874a453262b&password=uTb5-CYC%-WTqm-MBaY-!aAT-ApSq'

    response = requests.get(url=Full_url)

    dict = response.json()
    
    results = dict['results']
    
    hlrdata = results[0]

    if details['location'] != '':
        
        location = details['location']

        loc = {'location':location}

        hlrdata.update(loc)

    return hlrdata

 
if __name__ == "__main__":

    apilayerphone = 'cd3af5f7d1897dc1707c47d05c3759fd'

    phonenum = '+917010951718'

    HLRlookup(phonenum, apilayerphone)