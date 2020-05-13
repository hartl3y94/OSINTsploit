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
from .modules.social.locmap import loc,heat_map
from .modules.ip.ipstack import IPtrace
from .modules.ip.torrenttrack import GetTorrent
from .modules.ip.multipleip import read_multiple_ip
from .modules.phone.phonenum import HLRlookup
from .modules.ip.maclookup import macLookup
from .modules.email.hibp import HaveIbeenPwned
from .modules.email.hunter import hunter
from .modules.domain.webosint import getDomain
from .modules.ip.portscan import DefaultPort
from .modules.ip.censys import censys_ip
from .modules.ip.shodan import shodan_ip
import sys, os
import pdfx
from io import BufferedReader

sys.path.append("../src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@csrf_exempt
def index(request):

  if request.method == 'GET':
    return render(request, 'index.html')

  if request.method == 'POST':
    if "search" in request.POST.keys():
          return render(request, 'documentation.html',{'search':request.POST['search']})
    username = request.user.username
    user = User.objects.filter(username=username).first()

    ipstackkey = user.profile.ipstackkey
    macapikey = user.profile.macapikey
    hlrlookupkey = user.profile.hlrlookupkey
    hibpkey = user.profile.hibpkey
    hunterkey = user.profile.hunterkey
    googlemapapikey = user.profile.googlemapapikey
    shodankey = user.profile.shodankey
    
    query = str(request.POST['query'].replace(" ",""))
    query = query.split(":",1)
    if not len(query)<2:

      request_type = str(query[0])
      request_data = str(query[1])

      if request_type == 'facebook':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'twitter':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'instagram':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'social':
        return social(request, request_type, request_data, googlemapapikey)

      elif request_type == 'ip':
          ip={}
          ip['ipstackdata']= IPtrace(request_data, ipstackkey)
          ip['portscan']=DefaultPort(request_data)
          ip['censys']=censys_ip(request_data)
          ip['shodan']=shodan_ip(request_data,shodankey)
          
          lats = ip['ipstackdata']['latitude']
          lons = ip['ipstackdata']['longitude']
          
          ip['gmap3']=heat_map([lats],[lons],googlemapapikey)
          ip['torrentdata'] = GetTorrent(request_data)

          return render(request, 'results.html',{'ip':ip})

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
            return render(request,'results.html',{'hibp':hibp,'hunterio':hunterio})
      elif request_type == 'domain':
            return domain(request,request_data)
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

      if len(location)>0:
          gmap3=loc(location, googlemapapikey)
      else:
          gmap3=None

      return render(request, 'social.html',{'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata,'gmap3':gmap3})

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
  return render(request, 'documentation.html')

def about(request):
  return render(request, 'about.html')

@csrf_exempt
def settings(request):

  if request.method == 'GET':
   return render(request, 'settings.html')

  if request.method == 'POST':
        
    username = request.user.username

    user = User.objects.filter(username=username).first()

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

    user.profile.save()

    return render(request, 'settings.html')

@csrf_exempt
def logout(request):

  auth.logout(request)
  return HttpResponseRedirect("login")

@csrf_exempt
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
