import requests
import IP2Proxy, IP2Location
import gmplot
from io import BufferedReader
import json

def read_multiple_ip(ip_file,api_key):
    lats = []
    lons = []
    f = BufferedReader(ip_file).read()
    f1 = f.decode("utf-8").split("\n")[:-1]

    headers={
    'Host': 'api.ipstack.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie': '__cfduid=d8c577c3fc10b4d0faf72602bd1bef2861588930421',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    }

    for line in f1:
        r=requests.get("http://api.ipstack.com/" + line + "?access_key=" + api_key,headers=headers,verify=False)
        resp = r.json()
        if resp['latitude'] and resp['longitude']:
            lats.append(resp['latitude'])
            lons.append(resp['longitude'])
    return [lats,lons]#heat_map(lats,lons)

def heat_map(lats,lons):
    gmap3 = gmplot.GoogleMapPlotter(20.5937, 78.9629, 4)
    # Plot method Draw a line in
    # between given coordinates
    gmap3.heatmap(lats,lons)
    '''for i in range(len(lats)):
        gmap3.marker(lats[i],lons[i], 'cornflowerblue')'''
    gmap3.scatter(lats,lons, '#FF0000', size=50, marker=False)
    gmap3.plot(lats,lons, 'cornflowerblue', edge_width = 3.0)
    gmap3.apikey = "AIzaSyBnIrhidN5aiBFBVK9kgPDrISe0_MePQpw"
    gmap3.draw("templates/apps/heatmap.html")
    return gmap3
