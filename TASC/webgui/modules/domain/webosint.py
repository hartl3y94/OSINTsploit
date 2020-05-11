import  socket
import dns.resolver
from bs4 import BeautifulSoup
import requests, urllib,re
from PIL import Image

def getDomain(host, port=443):
    output={}    
    output['Whois']=GetWhois(host)
    output['DomainRecon']=DomainRecon(host,80)
    output['Nslookup']=nsLookup(host, port)
    output['Subdomains']=SubDomain(host, 443)
    output['CMS']=CMSdetect(host, port)
    output['Domain_Map']=DomainMap(host)
    return output

def GetWhois(host):
    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_zAh8wGadGEvLZQE9pTi1KWGLkL1oX&domainName="+host
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, features="lxml")
    data = soup.find('strippedtext').text
    temp={}
    data=data.split("\n")
    for i in data:
        try:
            t=i.split(":")
            temp[t[0]]=t[1]
        except:
            pass
    return temp

def DomainRecon(domain,port):
    temp={}
    if port == 80:
          port = 'http://'
    elif port == 443:
          port = 'https://'
    temp["Domain"]=domain
    temp["DomainRecord"]=DomainRecords(domain)
    temp["Header"]=getHeaders(port+domain)
    return temp

def getHeaders(domain):
    try:
        headers = requests.get(domain).headers
        server = ''
        output={}
        for key,value in headers.items():
            output[key]=value
        return output
    except:
        pass

def DomainRecords(domain):
    DomainRecords={}
    
    domain = str(domain)
    ip = []
    ipr = dns.resolver.query(domain, 'A')
    for rdata in ipr:
        ip.append(rdata.to_text())
    try:
        temp=[]
        for ip in ip:
            temp.append(getIPwhois(ip))
        DomainRecords['IP']=temp
    except:
        pass

    mxrecords = {}
    mxr = dns.resolver.query(domain, 'MX')
    i=1
    for rdata in mxr:
        mxrecords[i]=rdata.to_text()
        i+=1
    
    DomainRecords['Mxrecord']=mxrecords

    cname = {}
    try:
        cnamer = dns.resolver.query(domain, 'CNAME')
        i=1
        for rdata in cnamer:
            c[i]=rdata.to_text()
            i+=1
        DomainRecords['Cname']=cname
    except:
        pass
    return DomainRecords

def getIPwhois(ip):
    response = requests.get("https://ipapi.co/"+ip+"/json")
    resp = response.json()
    return resp

def nsLookup(host, port):
    reversed_dns = socket.gethostbyaddr(host)
    temp=[]
    i=1
    for z in reversed_dns:
        if z != None:
            temp.append(z)
        elif type(z)==type(list):
            temp.append(z[0])
    return temp

def CMSdetect(domain, port):
    payload = {'key': '1641c3b9f2b1c8676ceaba95d00f7cf2e3531830c5fa9a6cc5e2d922b2ed7165dcce66', 'url': domain}
    cms_url = "https://whatcms.org/APIEndpoint/Detect"
    try:
        response = requests.get(cms_url, params=payload)
        cms_data = response.json()
        cms_info = cms_data['result']
        output={}
        if cms_info['code'] == 200:
            output["Detected_CMS"]=cms_info['name']
            output["Detected_Version"]=cms_info['version']
            output["Confidence"]=cms_info['confidence']
        else:
            output["Message"]=cms_info['msg']
            output["Detected_CMS"]=cms_info['name']
            output["Detected_Version"]=cms_info['version']
        return output
    except:
        return "CMS Not Detected"
    
def SubDomain(host, port):
    host=host.replace('www.','')
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'

    params = {'apikey':'1af37bfeb7b1628ba10695fb187987a6651793e37df006a5cdf8786b0e4f6453','domain':host}

    response = requests.get(url, params=params)
    subdomains = response.json()
    temp=[]
    for x in subdomains['subdomains']:
        temp.append(x)
        
    return temp

def DomainMap(host):

    try :

        if 'www' in host:
            host = str(host)
            host = host.replace("www.",'')

        r = requests.get("https://dnsdumpster.com/")
        c = r.content

        soup = BeautifulSoup(c, 'lxml')

        csrf = soup.find('input').get('value')
        csrf.strip()

        headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Origin': 'https://dnsdumpster.com',
            'Upgrade-Insecure-Requests': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://dnsdumpster.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        data = {
          'csrfmiddlewaretoken': csrf,
          'targetip': host
        }

        cookies = {
            'csrftoken': csrf,
        }

        response = requests.post('https://dnsdumpster.com/', headers=headers, cookies=cookies, data=data)

        soup = BeautifulSoup(response.text, 'html.parser')

        dom_map = soup.find(attrs={"class": "img-responsive"})

        dom_map = str(dom_map)

        map_link = re.findall(r'src="(.*?)"', dom_map)

        for i in map_link:

            map_link = "https://dnsdumpster.com"+i

        return map_link
    
    except:
        pass