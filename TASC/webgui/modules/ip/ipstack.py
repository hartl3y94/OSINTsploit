import requests
import IP2Proxy, IP2Location
import gmplot
import sys, json, ast
import os



def IPtrace(ip, api_key):
    os.system('pwd')

    api_key = api_key

    database = IP2Location.IP2Location()

    database.open("webgui/modules/src/ipstack/IP2LOCATION-LITE-DB11.BIN")
    
    ipstackdata = str(database.get_all(ip))

    ipstackdata = ast.literal_eval(ipstackdata)

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

    lats = []
    lons = []

    r = requests.get("http://api.ipstack.com/" + ip + "?access_key=" + api_key)
    resp = r.json()

    if resp['latitude'] and resp['longitude']:

        lats = resp['latitude']
        lons = resp['longitude']

    latlon = {'latitude':lats,'longitude':lons}

    ipstackdata.update(latlon)

    return ipstackdata

    proxy.close()
    database.close()

    '''maps_url = "https://maps.google.com/maps?q=%s,+%s" % (lats, lons)
    openWeb = input("Open GPS location in web broser? (Y/N) ")
    if openWeb.upper() == 'Y':
        webbrowser.open(maps_url, new=2)
    else:
        print()
        return'''

#print(IPtrace("182.72.162.16","36f8692abc551f6c2939321d937c2a29"))
