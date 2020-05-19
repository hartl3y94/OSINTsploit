import requests
import IP2Proxy, IP2Location
import gmplot
import sys, json, ast
import os
import ipaddress


def IPtrace(ip, api_key):

    api_key = api_key
    lats = []
    lons = []

    if ":" in ip:
        response=requests.get("https://ipapi.co/"+ip+"/json/")
        ipstackdata = json.loads(response.text)
        
        lats = (ipstackdata['latitude'])
        lons = (ipstackdata['longitude'])
        
    else:

        database = IP2Location.IP2Location()

        database.open("webgui/modules/src/ipstack/IP2LOCATION-LITE-DB11.BIN")

        ipstackdata = str(database.get_all(ip))

        ipstackdata = ast.literal_eval(ipstackdata)
        

        r = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + api_key)
        resp = r.json()

        if resp['latitude'] and resp['longitude']:

            lats = resp['latitude']
            lons = resp['longitude']

    #print(type(ipstackdata))

    proxy = IP2Proxy.IP2Proxy()

    proxy.open("webgui/modules/src/ipstack/IP2PROXY-LITE-PX8.BIN")

    record = proxy.get_all(ip)

    isproxy = str(record['is_proxy'])

    if isproxy=='1':

        ipstackdata.update(record)

        return ipstackdata

    else:
        pass

    latlon = {'latitude':lats,'longitude':lons}
    ipstackdata.update(latlon)

    return ipstackdata

    proxy.close()
    database.close()

#print(IPtrace("182.72.162.16","36f8692abc551f6c2939321d937c2a29"))
