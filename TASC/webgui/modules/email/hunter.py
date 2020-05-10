import requests

def hunter(email,apikey):
    url="https://api.hunter.io/v2/email-verifier?email="+email+"&api_key="+apikey
    response=requests.get(url)
    if response.status_code==200:
        data=[]
        data=response.json()['data']['sources']
        data=[dict(t) for t in {tuple(d.items()) for d in data}]
        
        if len(data) == 0:
            return {'Error':'The Email is Not Breached'}
        else:
            return data
    else:
        return {'Error':'Something Went Wrong'}