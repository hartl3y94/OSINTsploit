import requests

def hunter(email,apikey):
    url="https://api.hunter.io/v2/email-verifier?email="+email+"&api_key="+apikey
    response=requests.get(url)
    if response.status_code==200:
        data=[]
        response=response.json()
        for i in response['data']['sources']:
            data.append(i['domain'])
        data=list(set(data))
        if len(data) == 0:
            return {'Error':'The Email is Not Breached'}
        else:
            return data
    else:
        return {'Error':'Something Went Wrong'}