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
from .ip.censys import Censys_ip
from .ip.shodan import shodan_ip
from .phone.phonenum import HLRlookup
from .email.hibp import HaveIbeenPwned
from .email.hunter import hunter
from .email.emailrep import emailrep
from .domain.webosint import getDomain
from django.contrib.auth.models import User
from .btc.btc import btcaddress
from .vechile.license import vechileno
import os
import json

def domainrecon(request,request_data):
    try:
      portscan=DefaultPort(request_data)
      web = getDomain(request_data)
    except:
      web=None
      portscan=None
    
    return {"webosint": web,'portscan':portscan}

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
        return {'twitterdata':twitterdata }

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
        if 'Error' not in instadata:
            if 'Location' in instadata.keys() and len(instadata['Location'])>0:
                for i in instadata['Location']:
                    location.append(i)
        else:
            instadata=None

        twitterdata = Twitter(request_data)
        if 'Error' not in twitterdata:
            if 'location' in twitterdata.keys() and twitterdata['location'] !="Not provided by the user":
                location.append(twitterdata["Location"])
            else:
                pass
        else:
            pass

        return {'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata}

    else:
        return


def MakeCluster(request,subquery):
    
    with open("templates/json/facebook.json","r") as f:
        data=json.loads(f.read())
        facebooknode=data['facebooknode']
        facebooklink=data['facebooklink']
        
    with open("templates/json/instagram.json","r") as f:
        data=json.loads(f.read())
        instanode=data['instanode']
        instalink=data['instalink']
    
    with open("templates/json/twitter.json","r") as f:
        data=json.loads(f.read())
        twitternode=data['twitternode']
        twitterlink=data['twitterlink']
            
    with open("templates/json/phone.json","r") as f:
        data=json.loads(f.read())
        phonenode=data['phonenode']
        phonelink=data['phonelink']  
    
    with open("templates/json/domain.json","r") as f:
        data=json.loads(f.read())
        domainnode=data['domainnode']
        domainlink=data['domainlink']
        
    with open("templates/json/email.json","r") as f:
        data=json.loads(f.read())
        emailnode=data['emailnode']
        emaillink=data['emaillink']
        
    with open("templates/json/mac.json","r") as f:
        data=json.loads(f.read())
        macnode=data['macnode']
        maclink=data['maclink']
        
    with open("templates/json/btc.json","r") as f:
        data=json.loads(f.read())
        btcnode=data['btcnode']
        btclink=data['btclink']
        
    with open("templates/json/ip.json","r") as f:
        data=json.loads(f.read())
        ipnode=data['ipnode']
        iplink=data['iplink']
        
    with open("templates/json/vehicle.json","r") as f:
        data=json.loads(f.read())
        vehiclenode=data['vehiclenode']
        vehiclelink=data['vehiclelink']
                
    #Blacklisted socialmedia websites         
    with open("webgui/modules/src/top250.txt") as f:
        weblist=f.read()
    weblist=weblist.split("\n")
    for i in weblist:
        if "http:" in i:
            weblist[weblist.index(i)]=i[7:].split("/")[0]
        else:
            weblist[weblist.index(i)]=i[8:].split("/")[0]
    username = request.user.username
    user = User.objects.filter(username=username).first()

    ipstackkey = user.profile.ipstackkey
    macapikey = user.profile.macapikey
    hlruname = user.profile.hlruname
    hlrpwd = user.profile.hlrpwd
    apilayerphone = user.profile.apilayerphone
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
                if 'Web_Link' in data['twitterdata'].keys() and data['twitterdata']['Web_Link']!=None and "No" not in data['twitterdata']['Web_Link']:
                    temp=data['twitterdata']['Web_Link']
                    if "http:" in temp:
                        temp=temp[7:].split("/")[0]
                    else:
                        temp=temp[8:].split("/")[0]
                    if temp not in weblist:
                        subquery.append("domain="+temp)
                        twitterlink.append({"source": "50","target": "8"})
            elif request_type == 'instagram':
                data.update(social(request, request_type, request_data))
            elif request_type == 'social':
                data.update(social(request, request_type, request_data))
                '''if data['fbdata']['Contact']:
                    subquery.append("domain="+data['fbdata']['Contact'])'''
                if 'Web_Link' in data['twitterdata'].keys() and data['twitterdata']['Web_Link']!=None and "No" not in data['twitterdata']['Web_Link']:
                    temp=data['twitterdata']['Web_Link']
                    if "http:" in temp:
                        temp=temp[7:].split("/")[0]
                    else:
                        temp=temp[8:].split("/")[0]
                    if temp not in weblist:
                        subquery.append("domain="+data['twitterdata']['Web_Link'])
                        twitterlink.append({"source": "50","target": "8"})
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
                    subquery.append("domain="+data["ip"]["ipstackdata"]["domain"])
                    iplink.append({"source": "50","target": "20"})

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
                    data.update({'btcdata':btc})
                
            elif request_type == 'fbsearch':
                    keyword=str(request.POST['query'].split(":")[-1])
                    fbsearch=FacebookScrapper(keyword,c_user,xs)
                    data.update({'fbsearch':fbsearch})
            elif request_type == 'vehicle':
                    vehicledata = vechileno(request_data)
                    data.update({'vehicle':vehicledata})
            else:
                pass

    clusterdata = {
    }

    if 'facebook' in query_list:
        
        if "fbdata" in data.keys():
            facebooknode[0]['description']={k:v for k,v in data['fbdata'].items() if k not in ["Current_city","Home_Town"]}
            try:
                facebooknode[1]['description']=data['fbdata']['Current_city']
                facebooknode[2]['description']=data['fbdata']['Home_Town']
            except:
                pass

            if clusterdata == {}:
                clusterdata['nodes'] = facebooknode
                clusterdata['links'] = facebooklink
            else:
                clusterdata['nodes'] += facebooknode
                clusterdata['links'] += facebooklink

    if 'instagram' in query_list:

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

        if "twitterdata" in data.keys():
            try:
                twitterweblink = data['twitterdata']['Web_Link']
                del data['twitterdata']['Web_Link']
            except:
                pass
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
        try:
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
        except:
            pass
    
    if 'email' in query_list:
    
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

    if 'ip' in query_list:
        
        length = len(ipnode)
        ipnode[0]['description']=data['ip']['ipstackdata']
        ipnode[1]['description']=data['ip']['censys']
        ipnode[2]['description']=data['ip']['portscan']

        if data['ip']['torrentdata'] != {}:
            ipnode[4]['description']=data['ip']['torrentdata']
            length = length-1

        else:
            del ipnode[length-1]
            del iplink[length-2]
            length = length-1
        
        try :
            if data['ip']['shodan'] != None:
                ipnode[3]['description']=data['ip']['shodan']
                length = length-1
            
        except:
            del ipnode[length-1]
            del iplink[length-2]

        if clusterdata == {}:
                clusterdata['nodes'] = ipnode
                clusterdata['links'] = iplink

        else:
            clusterdata['nodes'] += ipnode
            clusterdata['links'] += iplink
       
    if 'mac' in query_list:
    
        if "macdata" in data.keys():
            macnode[0]['description']=data['macdata']
            macnode[1]['description']=data['macdata']['Manufacturer']
            macnode[2]['description']=data['macdata']['Manufacturer_Address']
            if clusterdata == {}:
                clusterdata['nodes'] = macnode
                clusterdata['links'] = maclink

            else:
                clusterdata['nodes'] += macnode
                clusterdata['links'] += maclink
    
    if 'btc' in query_list:
        
        if "btcdata" in data.keys():
            btcnode[0]['description']={keys:values for keys,values in data['btcdata'].items() if keys != "transactions"}
            btcnode[1]['description']={i+1:data['btcdata']['transactions'][i] for i in range(len(data['btcdata']['transactions']))}
            
            if clusterdata == {}:
                clusterdata['nodes'] = btcnode
                clusterdata['links'] = btclink

            else:
                clusterdata['nodes'] += btcnode
                clusterdata['links'] += btclink
    
    if 'vehicle' in query_list:

        vehiclenode[1]['description']=data['vehicle']['Registering Authority']
        del data['vehicle']['Registering Authority']
        vehiclenode[0]['description']=data['vehicle']

        if clusterdata == {}:
                clusterdata['nodes'] = vehiclenode
                clusterdata['links'] = vehiclelink

        else:
            clusterdata['nodes'] += vehiclenode
            clusterdata['links'] += vehiclelink
        

    
    username = request.user.username
    user = User.objects.filter(username=username).first()
    user.profile.clusterjson=str(username)+".json"
    url = "/media/json/"+str(user.profile.clusterjson)
    user.save()
    with open("."+url,"w") as f:
        json.dump(clusterdata, f)
    return url

