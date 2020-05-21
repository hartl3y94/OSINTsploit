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

def domain(request,request_data):
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
    for i in subquery:
        temp_query=i.split("=")
        if not len(temp_query)<2:
            request_type = str(temp_query[0])
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
                    data.update({"domain":domain(request,request_data)})
                
            elif request_type == 'btc':
                    btc=btcaddress(request_data)
                    data.update({'btc':btc})
                
            elif request_type == 'fbsearch':
                    keyword=str(request.POST['query'].split(":")[-1])
                    fbsearch=FacebookScrapper(keyword,c_user,xs)
                    data.update({'fbsearch':fbsearch})
            else:
                pass
    with open("./media/json/data.json","r") as f:
        jsondata=json.loads(f.read())
    if "fbdata" in data.keys():
        jsondata['nodes'][0]['description']={k:v for k,v in data['fbdata'].items() if k not in ["Current_city","Home_Town"]}
        jsondata['nodes'][6]['description']=data['fbdata']['Current_city']
        jsondata['nodes'][7]['description']=data['fbdata']['Home_Town']
    if "instadata" in data.keys():
        jsondata['nodes'][1]['description']=data['instadata']
    if "twitterdata" in data.keys():
        jsondata['nodes'][2]['description']=data['twitterdata']
    if "hlrdata" in data.keys():
        jsondata['nodes'][3]['description']=data['hlrdata']
    if "domain" in data.keys():
        jsondata['nodes'][4]['description']=data['domain']
    if "ip" in data.keys():
        jsondata['nodes'][5]['description']=data['ip']
    username = request.user.username
    user = User.objects.filter(username=username).first()
    print(User.objects.filter(username=username).first().profile.clusterjson)
    user.profile.clusterjson=str(username)+".json"
    url = "/media/json/"+str(user.profile.clusterjson)
    user.save()
    with open("."+url,"w") as f:
        json.dump(jsondata, f)
    return url

