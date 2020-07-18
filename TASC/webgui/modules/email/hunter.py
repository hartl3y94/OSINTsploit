import requests

def hunter(email,apikey):
    url="https://api.hunter.io/v2/email-verifier?email="+email+"&api_key="+apikey
    response=requests.get(url)
    if response.status_code==200:
        hunterdata={}
        hunterdata=response.json()
        
        if len(hunterdata) == 0:
            return {'Error':'The Email is Not Breached'}
        else:
            return hunterdata
    else:
        return None