
from .censys import Censys_ip
from .ipstack import IPtrace
from .maclookup import macLookup
from .portscan import DefaultPort
from .shodan import shodan_ip
from .torrenttrack import GetTorrent


def Ipaddress(request_data, ipstackkey, shodankey):


    ip = IPtrace(request_data, ipstackkey)

    portscandata = DefaultPort(request_data)
    if portscandata:
        ip['portscan'] = portscandata

    censysdata = censys_ip(request_data)
    if censysdata:
        ip['censys'] = censysdata

    shodandata = shodan_ip(request_data, shodankey)
    if shodandata:
        ip['shodan'] = shodandata

    torrentdata = GetTorrent(request_data)
    if torrentdata:
        ip['torrentdata'] = torrentdata
 
    return ip

      
