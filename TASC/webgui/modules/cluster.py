from .social.facebook import Facebook
from .social.instagram import Instagram
from .social.twitter import Twitter
from .social.fbkeyword import FacebookScrapper
from .social.locmap import loc,heat_map, gps_map
from .ip.ipstack import IPtrace
from .ip.torrenttrack import GetTorrent
from .ip.multipleip import read_multiple_ip
from .ip.maclookup import macLookup
from .ip.portscan import DefaultPort
from .ip.censys import censys_ip
from .ip.shodan import shodan_ip
from .phone.phonenum import HLRlookup
from .email.hibp import HaveIbeenPwned
from .email.hunter import hunter
from .email.emailrep import emailrep
from .domain.webosint import getDomain
from django.contrib.auth.models import User
from .btc.btc import btcaddress
import os
import json

def domainrecon(request,request_data):
      portscan=DefaultPort(request_data)
      return {"webosint":getDomain(request_data),'portscan':portscan}

def social(request, request_type, request_data):

  request_type = request_type
  request_data = request_data

  if request_type == 'facebook':
    fbdata = Facebook(request_data)
    return {'fbdata':fbdata}

  elif request_type == 'instagram':
      instadata = Instagram(request_data)
      return {'instadata':instadata}

  elif request_type == 'twitter':

      twitterdata = Twitter(request_data)
      return {'twitterdata':twitterdata}

  elif request_type == 'social':
      location=list()
      try:
          fbdata = Facebook(request_data)
          if fbdata["Current_city"]:
              location.append(fbdata["Current_city"])
          if fbdata["Home_Town"]:
              location.append(fbdata["Home_Town"])
      except:
          fbdata=None

      instadata = Instagram(request_data)
      if 'Error' not in instadata.keys() and ['Error']!='Profile not found':
          if 'Location' in instadata.keys() and len(instadata['Location'])>0:
              for i in instadata['Location']:
                  location.append(i)
      else:
          instadata=None

      twitterdata = Twitter(request_data)
      if twitterdata!=None:
          if 'location' in twitterdata.keys() and twitterdata['location'] !="Not provided by the user":
              location.append(twitterdata["Location"])
          else:
              pass
      else:
          twitterdata=None
          
      return {'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata}
  else:
    return


def MakeCluster(request,subquery):
    username = request.user.username
    user = User.objects.filter(username=username).first()

    ipstackkey = user.profile.ipstackkey
    macapikey = user.profile.macapikey
    hlrlookupkey = user.profile.hlrlookupkey
    hibpkey = user.profile.hibpkey
    hunterkey = user.profile.hunterkey
    googlemapapikey = user.profile.googlemapapikey
    shodankey = user.profile.shodankey
    emailrepkey = user.profile.emailrepkey
    c_user = user.profile.c_user
    xs = user.profile.xs
    data={}
    query_list = []
    for i in subquery:
        temp_query=i.split("=")
        if not len(temp_query)<2:
            request_type = str(temp_query[0])
            query_list.append(request_type)
            request_data = str(temp_query[1])
            if request_type == 'facebook':
                data.update(social(request, request_type, request_data))
                '''if data['fbdata']['Contact']:
                    subquery.append("domain="+data['fbdata']['Contact'])'''
            elif request_type == 'twitter':
                data.update(social(request, request_type, request_data))
                '''if data['twitterdata']['Web_Link']!=None and "http" in data['twitterdata']['Web_Link']:
                    subquery.append("domain="+data['twitterdata']['Web_Link'])'''
            elif request_type == 'instagram':
                data.update(social(request, request_type, request_data))
            elif request_type == 'social':
                data.update(social(request, request_type, request_data))
                '''if data['fbdata']['Contact']:
                    subquery.append("domain="+data['fbdata']['Contact'])
                if data['twitterdata']['Web_Link']!=None and "http" in data['twitterdata']['Web_Link']:
                    subquery.append("domain="+data['twitterdata']['Web_Link'])'''
            elif request_type == 'ip':
                ip={}
                ip['ipstackdata']= IPtrace(request_data, ipstackkey)
                portscandata = DefaultPort(request_data)
                if portscandata['Ports'] :
                    ip['portscan']=portscandata

                censysdata = censys_ip(request_data)
                if censysdata :
                    ip['censys']=censysdata

                shodandata = shodan_ip(request_data,shodankey)
                if 'Error' not in shodandata.keys():
                    ip['shodan']=shodandata
                
                ip['torrentdata'] = GetTorrent(request_data)

                data.update({'ip':ip})
                if data["ip"]["ipstackdata"]["domain"] != None:
                    subquery.append("domain="+data['twitterdata']['Web_Link'])

            elif request_type == 'phone':
                try:
                    hlrdata = HLRlookup(request_data, hlrlookupkey)
                    data.update({'hlrdata':hlrdata})
                except:
                    pass

            elif request_type == 'mac':
                if len(request_data)==17 and len(request_data.split(":"))==6:
                    macdata = macLookup(request_data, macapikey)
                    if 'Error' in macdata.keys():
                        pass
                    else:
                        data.update({'macdata':macdata})
                else:
                    pass

            elif request_type == 'email':
                    hibp=HaveIbeenPwned(request_data,hibpkey)
                    hunterio=hunter(request_data,hunterkey)
                    emailrepdata=emailrep(request_data,emailrepkey)
                    data.update({'hibp':hibp,'hunterio':hunterio,'emailrep':emailrepdata})
          
                    
            elif request_type == 'domain':
                    domaindata=domainrecon(request,request_data)
                    data.update({"domain":domaindata})
                
            elif request_type == 'btc':
                    btc=btcaddress(request_data)
                    data.update({'btc':btc})
                
            elif request_type == 'fbsearch':
                    keyword=str(request.POST['query'].split(":")[-1])
                    fbsearch=FacebookScrapper(keyword,c_user,xs)
                    data.update({'fbsearch':fbsearch})
            else:
                pass

    clusterdata = {
    }

    if 'facebook' in query_list:
        
        facebooknode = [
            {
            "id": "1",
            "module": "Facebook",
            "description": "",
            "group": 1  
            },
            {
            "id": "2",
            "module": "Current City",
            "description": "",
            "group": 1  
            },
            {
            "id": "3",
            "module": "Home Town",
            "description": "",
            "group": 1  
            },
            
        ]

        facebooklink = [
            {
            "source": "2",
            "target": "1"
            },

            {
            "source": "3",
            "target": "1"
            },
        ]   

        if "fbdata" in data.keys():
            facebooknode[0]['description']={k:v for k,v in data['fbdata'].items() if k not in ["Current_city","Home_Town"]}
            facebooknode[1]['description']=data['fbdata']['Current_city']
            facebooknode[2]['description']=data['fbdata']['Home_Town']

            if clusterdata == {}:
                clusterdata['nodes'] = facebooknode
                clusterdata['links'] = facebooklink
            else:
                clusterdata['nodes'] += facebooknode
                clusterdata['links'] += facebooklink

    if 'instagram' in query_list:

        instanode =  [
        {
            "id": "4",
            "module": "Instagram",
            "description": "",
            "group": 2
        },

        {
            "id": "5",
            "module": "Locations",
            "description": "",
            "group": 2
        },

        ]

        instalink = [
        {
            "source": "5",
            "target": "4"
        },
        ]


        if "instadata" in data.keys():
            instalocation = data['instadata']['Location']
            del data['instadata']['Location']
            instanode[0]['description']=data['instadata']
            instanode[1]['description']=instalocation

            if clusterdata == {}:
                clusterdata['nodes'] = instanode
                clusterdata['links'] = instalink
            else:
                clusterdata['nodes'] += instanode
                clusterdata['links'] += instalink


    if 'twitter' in query_list:

        twitternode = [
        {
            "id": "6",
            "module": "Twitter",
            "description": "",
            "group": 3
        },

        {
            "id": "7",
            "module": "Twitter Location",
            "description": "",
            "group": 3
        },

        {
            "id": "8",
            "module": "Twitter Weblink",
            "description": "",
            "group": 3
        },

        ]

        twitterlink = [
        {
            "source": "7",
            "target": "6"
        },

        {
            "source": "8",
            "target": "6"
        },
        ]

        if "twitterdata" in data.keys():
            twitterweblink = data['twitterdata']['Web_Link']
            del data['twitterdata']['Web_Link']
            twitterlocation = data['twitterdata']['Location']
            del data['twitterdata']['Location']
            twitternode[0]['description']=data['twitterdata']
            twitternode[1]['description']=twitterlocation
            twitternode[2]['description']=twitterweblink

            if clusterdata == {}:
                clusterdata['nodes'] = twitternode
                clusterdata['links'] = twitterlink

            else:
                clusterdata['nodes'] += twitternode
                clusterdata['links'] += twitterlink

    if 'phone' in query_list:

        phonenode = [
        {
            "id": "9",
            "module": "Phone",
            "description": "",
            "group": 4
        },

        {
            "id": "10",
            "module": "Location",
            "description": "",
            "group": 4
        },

        {
            "id": "11",
            "module": "Roaming",
            "description": "",
            "group": 4
        },

        {
            "id": "12",
            "module": "Ported",
            "description": "",
            "group": 4
        },

        {
            "id": "13",
            "module": "ACT",
            "description": "",
            "group": 4
        },

        ]

        phonelink = [
        {
            "source": "10",
            "target": "9"
        },

        {
            "source": "11",
            "target": "9"
        },

        {
            "source": "12",
            "target": "9"
        },

        {
            "source": "13",
            "target": "9"
        },
        ]

        if "hlrdata" in data.keys():

            phonedata = {}
            
            if data['hlrdata']['subscriberstatus'] == 'SUBSCRIBERSTATUS_CONNECTED':
                phonedata['Subscriber Status'] = 'Connected'

            else:
                phonedata['Subscriber Status'] = data['hlrdata']['subscriberstatus']

            phonedata['IMSI'] = data['hlrdata']['imsi']
            phonedata['MCC MNC'] = data['hlrdata']['mccmnc']
            phonedata['Original Network'] = data['hlrdata']['originalnetworkname']
            hlrlocation = {}
            hlrlocation['State'] = data['hlrdata']['location']
            hlrlocation['Country'] = data['hlrdata']['originalcountryname']

            phonenode[0]['description']=phonedata
            phonenode[1]['description']=hlrlocation

            length = len(phonelink) 
             
            if data['hlrdata']['Account_Id']:
                actdata = {}
                actdata['Account ID'] = data['hlrdata']['Account_Id']
                actdata['Subscriber Name'] = data['hlrdata']['Subscriber_Name']
                actdata['Bill No.'] = data['hlrdata']['Bill_No']
                actdata['Previous Due'] = data['hlrdata']['Previous_Due']
                actdata['Current Invoice'] = data['hlrdata']['Current_Invoince']
                actdata['Total Payment Due'] = data['hlrdata']['Total_Payment_Due']
                phonenode[4]['description']=actdata
                length = length-1

            else:
                del phonelink[length-1] 
                del phonenode[length]
                length = length-1 

            if data['hlrdata']['isported'] == 'Yes':
                ported = {}
                ported['Ported Network name'] = data['hlrdata']['portednetworkname']
                ported['Ported Country name'] = data['hlrdata']['portedcountryname']
                phonenode[3]['description']=ported
                length = length-1 

            else:
                del phonelink[length-1] 
                del phonenode[length]
                length = length-1
            
            if data['hlrdata']['isroaming'] == 'Yes':
                roaming = {}
                roaming['Roaming Network'] = data['hlrdata']['roamingnetworkname']
                roaming['Roaming Country'] = data['hlrdata']['roamingcountryname']
                phonenode[2]['description']=roaming
            
            else:
                del phonelink[length-1]
                del phonenode[length]
                length = length-1 

            if clusterdata == {}:
                clusterdata['nodes'] = phonenode
                clusterdata['links'] = phonelink

            else:
                clusterdata['nodes'] += phonenode
                clusterdata['links'] += phonelink

    if "domain" in query_list:
        domainnode = [
        {
            "id": "50",
            "module": "Whois",
            "description": "",
            "group": 10
        },
        {
            "id": "51",
            "module": "DomainRecon",
            "description": "",
            "group": 10
        },
        {
            "id": "52",
            "module": "portscan",
            "description": "",
            "group": 10
        },
        {
            "id": "53",
            "module": "Nslookup",
            "description": "",
            "group": 10
        },
        {
            "id": "54",
            "module": "Subdomains",
            "description": "",
            "group": 10
        },
        {
            "id": "55",
            "module": "DomainRecord",
            "description": "",
            "group": 10
        },
        {
            "id": "56",
            "module": "Mxrecord",
            "description": "",
            "group": 10
        },
        {
            "id": "57",
            "module": "CMS",
            "description": "",
            "group": 10
        },
        ]

        domainlink = [
        {
            "source": "51",
            "target": "50"
        },
        {
            "source": "52",
            "target": "50"
        },
        {
            "source": "53",
            "target": "50"
        },
        {
            "source": "54",
            "target": "50"
        },
        {
            "source": "55",
            "target": "51"
        },
        {
            "source": "56",
            "target": "51"
        },
        {
            "source": "57",
            "target": "51"
        },
        ]
        data['domain']['webosint']['Whois']['ProfilePic']=data['domain']['webosint']['Domain_Map']
        domainnode[0]['description']=data['domain']['webosint']['Whois']
        domainnode[1]['description']=data['domain']['webosint']['DomainRecon']['Domain']
        domainnode[2]['description']=data['domain']['portscan']['Ports']
        ns={}
        for i in range(len(data['domain']['webosint']['Nslookup'])):
            ns[i+1]=data['domain']['webosint']['Nslookup'][i]
        domainnode[3]['description']=ns
        sub={}
        for i in range(len(data['domain']['webosint']['Subdomains'])):
            sub[i+1]=data['domain']['webosint']['Subdomains'][i]
        domainnode[4]['description']=sub
        
        domainnode[5]['description']=data['domain']['webosint']['DomainRecon']['DomainRecord']['IP'][0]
        domainnode[6]['description']=data['domain']['webosint']['DomainRecon']['DomainRecord']['Mxrecord']
        domainnode[7]['description']=data['domain']['webosint']['CMS']
        
        if clusterdata == {}:
            clusterdata['nodes'] = domainnode
            clusterdata['links'] = domainlink
        else:
            clusterdata['nodes'] += domainnode
            clusterdata['links'] += domainlink
    
    if 'email' in query_list:
    
        emailnode = [
        {
            "id": "14",
            "module": "Have I Been Pwned",
            "description": "",
            "group": 5
        },

        {
            "id": "15",
            "module": "Hunter IO",
            "description": "",
            "group": 5
        },

        {
            "id": "16",
            "module": "Email Rep",
            "description": "",
            "group": 5
        },

        {
            "id": "17",
            "module": "Details",
            "description": "",
            "group": 5
        },

        {
            "id": "18",
            "module": "Profiles",
            "description": "",
            "group": 5
        },

        {
            "id": "19",
            "module": "Sources",
            "description": "",
            "group": 5
        },


        ]

        emaillink = [
        {
            "source": "15",
            "target": "14"
        },

        {
            "source": "16",
            "target": "14"
        },

        {
            "source": "17",
            "target": "16"
        },

        {
            "source": "18",
            "target": "16"
        },

        {
            "source": "19",
            "target": "15"
        },
        ]

        if 'Error' in data['hibp']:
            emailnode[0]['description']=data['hibp']
        else:
            breached = {}
            domains = []
            for domain in data['hibp']:
                domains.append(domain['Name'])
            breached['Breached Domains'] = domains
            emailnode[0]['description'] = breached['Breached Domains']
        emailnode[1]['description'] = data['hunterio']['data']['sources']
        del data['hunterio']['data']['sources']
        emailnode[1]['description']=data['hunterio']['data']
        emailnode[4]['description']=data['emailrep']['details']['profiles']
        del data['emailrep']['details']['profiles']
        emailnode[3]['description']=data['emailrep']['details']
        del data['emailrep']['details']
        emailnode[2]['description']=data['emailrep']

        if clusterdata == {}:
                clusterdata['nodes'] = emailnode
                clusterdata['links'] = emaillink

        else:
            clusterdata['nodes'] += emailnode
            clusterdata['links'] += emaillink
                
    username = request.user.username
    user = User.objects.filter(username=username).first()
    user.profile.clusterjson=str(username)+".json"
    url = "/media/json/"+str(user.profile.clusterjson)
    user.save()
    with open("."+url,"w") as f:
        json.dump(clusterdata, f)
    return url

