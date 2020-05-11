import  socket
import dns.resolver
from bs4 import BeautifulSoup
import requests, urllib,re
from PIL import Image

def getDomain(host, port=443):
    output={}
    output={'Whois': {'Domain Name': ' skcet.ac.in', 'Registrar URL': ' http', 'Updated Date': ' 2019-06-11T05', 'Creation Date': ' 2004-06-30T04', 'Registry Expiry Date': ' 2024-06-30T04', 'Registrar': ' ERNET India', 'Registrar IANA ID': ' 800068', 'Domain Status': ' ok http', 'Registrant Organization': ' SRI KRISHNA COLLEGE OF ENGINEERING AND TECHNOLOGY', 'Registrant Country': ' IN', 'Registrant Email': ' Please contact the Registrar listed above', 'Admin Email': ' Please contact the Registrar listed above', 'Tech Email': ' Please contact the Registrar listed above', 'Name Server': ' ns37.domaincontrol.com'}, 'DomainRecon': {'Domain': 'www.skcet.ac.in', 'DomainRecord': {'IP': {'ip': '50.62.160.129', 'city': 'Scottsdale', 'region': 'Arizona', 'region_code': 'AZ', 'country': 'US', 'country_code': 'US', 'country_code_iso3': 'USA', 'country_capital': 'Washington', 'country_tld': '.us', 'country_name': 'United States', 'continent_code': 'NA', 'in_eu': False, 'postal': '85260', 'latitude': 33.6013, 'longitude': -111.8867, 'timezone': 'America/Phoenix', 'utc_offset': '-0700', 'country_calling_code': '+1', 'currency': 'USD', 'currency_name': 'Dollar', 'languages': 'en-US,es-US,haw,fr', 'country_area': 9629091.0, 'country_population': 310232863.0, 'asn': 'AS26496', 'org': 'AS-26496-GO-DADDY-COM-LLC'}, 'Mxrecord': {1: '1 aspmx.l.google.com.', 2: '5 alt1.aspmx.l.google.com.', 3: '5 alt2.aspmx.l.google.com.', 4: '10 alt3.aspmx.l.googlemail.com.', 5: '10 alt4.aspmx.l.googlemail.com.'}}, 'Header': {'Content-Type': 'text/html', 'Last-Modified': 'Thu, 07 May 2020 07:17:47 GMT', 'Accept-Ranges': 'bytes', 'ETag': '"2545f89b3f24d61:0"', 'Server': 'Microsoft-IIS/8.0', 'X-Powered-By': 'ASP.NET', 'X-Powered-By-Plesk': 'PleskWin', 'Date': 'Mon, 11 May 2020 15:13:55 GMT', 'Content-Length': '103920'}}, 'Nslookup': {1: 'p3nwvpweb108.shr.prod.phx3.secureserver.net', 2: [], 3: ['50.62.160.129']}, 'Subdomains': {1: 'placement.skcet.ac.in', 2: 'results.skcet.ac.in', 3: 'www.skcet.ac.in', 4: 'result2k18.skcet.ac.in', 5: 'intmark.skcet.ac.in', 6: 'hallticket.skcet.ac.in'}, 'CMS': {'Message': 'Failed: CMS or Host Not Found', 'Detected_CMS': None, 'Detected_Version': None}, 'Domain_Map': 'https://dnsdumpster.com/static/map/skcet.ac.in.png'}
    return output
    output['Whois']=GetWhois(host)
    output['DomainRecon']=DomainRecon(host,80)
    output['Nslookup']=nsLookup(host, port)
    output['Subdomains']=SubDomain(host, 443)
    output['CMS']=CMSdetect(host, port)
    output['Domain_Map']=DomainMap(host)
    print(output)
    return output

def GetWhois(host):
    url = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_zAh8wGadGEvLZQE9pTi1KWGLkL1oX&domainName="+host
    response = requests.get(url)
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
    output={}
    
    domain = str(domain)
    ip = []
    ipr = dns.resolver.query(domain, 'A')
    for rdata in ipr:
        ip.append(rdata.to_text())
    try:
        temp={}
        for ip in ip:
            temp[ip]=getIPwhois(ip)
        output['IP']=temp[ip]
    except:
        pass

    mxrecords = {}
    mxr = dns.resolver.query(domain, 'MX')
    i=1
    for rdata in mxr:
        mxrecords[i]=rdata.to_text()
        i+=1
    
    output['Mxrecord']=mxrecords

    cname = {}
    try:
        cnamer = dns.resolver.query(domain, 'CNAME')
        i=1
        for rdata in cnamer:
            c[i]=rdata.to_text()
            i+=1
        output['Cname']=cname
    except:
        pass
    return output

def getIPwhois(ip):
    response = requests.get("https://ipapi.co/"+ip+"/json")
    resp = response.json()
    return resp

def nsLookup(host, port):
    reversed_dns = socket.gethostbyaddr(host)
    temp={}
    i=1
    for z in reversed_dns:
        temp[i]=z
        i+=1
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
    temp={}
    i = 1
    for x in subdomains['subdomains']:
        temp[i]=x
        i = i+1
        
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