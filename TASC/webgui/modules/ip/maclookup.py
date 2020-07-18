import requests

def macLookup(mac,apikey):
    data={}
    url =  "https://api.macvendors.com/v1/lookup/"+mac

    api_key = "Bearer "+ apikey
    headers = {
    'Authorization': api_key,
    }
    resp = requests.get(url,headers=headers)
    result = resp.json()
    if resp.status_code == 200:
        final = result['data']
        data["Manufacturer"]= final['organization_name']
        data["Manufacturer_Address"]=final['organization_address']
    else:
        data["Error"]="MAC Address not found"
    return data
