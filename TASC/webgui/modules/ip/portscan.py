import nmap
import json

def DefaultPort(Xhost):
    nm = nmap.PortScanner()
    result = nm.scan(Xhost, '22-443')
    return display(result)

def display(result):

    scan={}
    try:
        new = next(iter(result['scan'].values()))
        scan['IP'] = new['addresses']
        scan['hostnames']=new['hostnames']
        scan['Ports'] = new['tcp']
    except:
        return None
    return scan
