import requests
import json


def TrueCaller(phonenum):

    url = "https://search5-noneu.truecaller.com/v2/search"

    headers = {

        'User-Agent':'Truecaller/11.7.5 (Android;6.0)',
        'Host':'search5-noneu.truecaller.com',
        'Accept':'application/json, text/plain, */*',
        'Authorization':'Bearer a1i0q--M8K9-NF2F0SYaWExyNTIjmOuUBgNNqOKHoVfoijj45zK1SUG5z5Xir3ih',
        'Clientsecret':'lvc22mp3l1sfv6ujg83rd17btt',
        'Content-Type':'application/json',
        'Connection':'close'
    }

    params = {
        'q':phonenum,
        'countryCode': 'IN',
        'type': 4,
        'locAddr': '',
        'placement': 'SEARCHRESULTS,HISTORY,DETAILS',
        'encoding': 'json'
    }

    response = requests.get(url=url, headers=headers, params=params).json()

    response = response['data'][0]
    details = {}
    if 'name' in response:
        details['name'] = response['name']
    if 'gender' in response:
        details['gender'] = response['gender']
    if 'email' in response:
        details['email'] = response['email']
    if 'image' in response:
        details['imgurl'] = response['image']
    if 'jobTitle' in response:
        details['job'] = response['jobTitle']
    if 'score' in response:
        details['truescore'] = response['score']
    if 'companyName' in response:
        details['company'] = response['companyName']
    try:
        details['domain'] = response['internetAddresses'][0]['id']
    except:
        pass
    try:
        details['isverfied'] = response['badges'][0]
    except:
        pass
    if response['spamInfo'] == {}:
        details['isspam'] = False
    else: 
        details['isspam'] = True

    return details    
    

#print(TrueCaller("7708687307"))