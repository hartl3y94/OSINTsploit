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
from .modules.social.locmap import loc,heat_map
from .modules.ip.ipstack import IPtrace
from .modules.ip.multipleip import read_multiple_ip
from .modules.phone.phonenum import HLRlookup
from .modules.ip.maclookup import macLookup
import sys
sys.path.append("../src")


@csrf_exempt
def index(request):

  if request.method == 'GET':
    return render(request, 'index.html')

  if request.method == 'POST':

    username = request.user.username
    user = User.objects.filter(username=username).first()

    ipstackkey = user.profile.ipstackkey
    macapikey = user.profile.macapikey
    hlrlookupkey = user.profile.hlrlookupkey

    query = str(request.POST['query'])
    query = query.split(":")

    if not len(query)<2:

      request_type = str(query[0])
      request_data = str(query[1])

      if request_type == 'facebook':
        return social(request, request_type, request_data)

      elif request_type == 'twitter':
        return social(request, request_type, request_data)

      elif request_type == 'instagram':
        return social(request, request_type, request_data)

      elif request_type == 'social':
        return social(request, request_type, request_data)

      elif request_type == 'ip':

          ipstackdata = IPtrace(request_data, ipstackkey)
          lats = ipstackdata['latitude']
          lons = ipstackdata['longitude']
          gmap3=heat_map([lats],[lons])
          return render(request, 'results.html',{'ipstackdata':ipstackdata,'gmap3':gmap3})

      elif request_type == 'phone':

          hlrdata = HLRlookup(request_data, hlrlookupkey)
          return render(request, 'results.html',{'hlrdata':hlrdata})

      elif request_type == 'mac':
          if len(query[1:])==6:
              mac=':'.join(query[1:])
              macdata = macLookup(mac, macapikey)
              if 'Error' in macdata.keys():
                  return render(request,'result.html',{'Error':macdata['Error']})
              else:
                  return render(request, 'results.html',{'macdata':macdata})
          else:
              return render(request,'index.html',{'error':"Invalid Mac Address"})

    else:
      error = 'The requested Query is INVALID'
      return render(request, 'index.html', {'error':error})


def social(request, request_type, request_data):

  request_type = request_type
  request_data = request_data

  if request_type == 'facebook':

    fbdata = Facebook(request_data)
    return render(request, 'social.html',{'fbdata':fbdata})

  elif request_type == 'instagram':
      instadata = Instagram(request_data)
      if 'Location' in instadata.keys() and len(instadata['Location']) >0:
          gmap3=loc(instadata['Location'])
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
          gmap3=loc(location)
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
        if 'input-b2' in request.FILES.keys():
            if request.FILES['input-b2'] != "":
                url=reverseImg(str(request.FILES['input-b2']),request.FILES['input-b2'].file)
                if "https" in url:
                    return redirect(url)
                else:
                    return render(request, 'modules.html',{"Error":url})
            else:
                return render(request, 'modules.html',{"Error":"Do Select the File"})

        elif 'input-b1' in request.FILES.keys():
            if request.FILES['input-b1'] != "":
                username = request.user.username
                user = User.objects.filter(username=username).first()
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

    if request.POST['hlrlookupkey'] != '':
      user.profile.hlrlookupkey = request.POST['hlrlookupkey']

    if request.POST['googleapikey'] != '':
      user.profile.googleapikey = request.POST['googleapikey']

    if request.POST['macapikey'] != '':
      user.profile.macapikey = request.POST['macapikey']

    if request.POST['ipstackkey'] != '':
      user.profile.ipstackkey = request.POST['ipstackkey']

    if request.POST['virustotalkey'] != '':
      user.profile.virustotalkey = request.POST['virustotalkey']

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
