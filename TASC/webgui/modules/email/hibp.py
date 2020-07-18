import requests
import json

def HaveIbeenPwned(email,apikey):
    url = "https://haveibeenpwned.com/api/v3/breachedaccount/"+email
    header = {'hibp-api-key': apikey}
    rqst = requests.get(url,headers=header,timeout=10)
    sc = rqst.status_code
    if sc == 200:
        json_out = rqst.content.decode('utf-8', 'ignore')
        simple_out = json.loads(json_out)
        return simple_out
    
    elif sc == 404:
        return {'Error':'The Email is Not Breached'}
        
    else:
        return None

