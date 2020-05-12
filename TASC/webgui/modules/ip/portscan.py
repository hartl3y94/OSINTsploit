import nmap
import json

def DefaultPort(Xhost):
    nm = nmap.PortScanner()
    result = nm.scan(Xhost, '22-443')
    return display(result)

def display(result):
    new = next(iter(result['scan'].values()))
    scan={}
    scan['IP'] = new['addresses']
    scan['hostnames']=new['hostnames']
    try:
        scan['Ports'] = new['tcp']
    except:
        scan['Ports'] = None
    return scan
