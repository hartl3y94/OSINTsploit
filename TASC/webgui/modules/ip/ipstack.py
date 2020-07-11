import requests
import IP2Proxy, IP2Location
import gmplot
import sys, json, ast
import os
import ipaddress

ipstack_dir = os.path.dirname(os.path.dirname((os.path.abspath(__file__))))

def IPtrace(ip, api_key):

    api_key = api_key
    lats = []
    lons = []

    response=requests.get("https://ipapi.co/"+ip+"/json/")
    ipapidata = json.loads(response.text)
    
    if ":" in ip: 
         
        lats = (ipapidata['latitude'])
        lons = (ipapidata['longitude'])
        
    else:

        database = IP2Location.IP2Location()

        database.open(ipstack_dir+"/src/ipstack/IP2LOCATION-LITE-DB11.BIN")

        ipstackdata = str(database.get_all(ip))

        ipstackdata = ast.literal_eval(ipstackdata)
        

        r = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + api_key)
        resp = r.json()

        if resp['latitude'] and resp['longitude']:

            lats = resp['latitude']
            lons = resp['longitude']

    #print(type(ipstackdata))

    proxy = IP2Proxy.IP2Proxy()

    proxy.open(ipstack_dir+"/src/ipstack/IP2PROXY-LITE-PX8.BIN")

    record = proxy.get_all(ip)

    isproxy = str(record['is_proxy'])

    if isproxy=='1':

        ipstackdata.update(record)

    else:
        pass

    latlon = {'latitude':lats,'longitude':lons}
    ipstackdata.update(latlon)

    return {"ipapi":ipapidata,"ipstackdata":ipstackdata}


#print(IPtrace("182.72.162.16","36f8692abc551f6c2939321d937c2a29"))
