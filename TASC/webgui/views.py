from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from .modules.social.facebook import Facebook
from .modules.social.instagram import Instagram
from .modules.social.twitter import Twitter
from .modules.social.tinder import tinder
from .modules.social.accounts import whatismyname
from .modules.social.tiktok import tiktok
from .modules.social.gravatar import gravatar
from .modules.social.medium import medium
from .modules.social.pinterest import pinterest
from .modules.social.keybase import keybase
from .modules.image.reverseimg import reverseImg
from .modules.image.metadata import get_exif
from .modules.social.locmap import loc,heat_map, gps_map
from .modules.ip.ipstack import IPtrace
from .modules.ip.torrenttrack import GetTorrent
from .modules.ip.multipleip import read_multiple_ip
from .modules.phone.phonenum import HLRlookup, numverify
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
from .modules.phone.getcontact import getcontact
from .modules.email.ghostproject import ghostproject

from django.http import JsonResponse
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from weasyprint import HTML
import tempfile

import sys, os,requests
import pdfx
from io import BufferedReader,BytesIO
import base64, json
import urllib.parse,urllib3
from datetime import datetime,timezone
import re, time
from xhtml2pdf import pisa
import pdfkit, asyncio
from pyvirtualdisplay import Display
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from threading import Thread
import time, asyncio
from dateutil import tz

sys.path.append("../src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):

  if request.method == 'GET':
    return render(request, 'index.html')
  if request.method == 'POST':
    username = request.user.username
    try:
      with open("media/json/history_{}.json".format(username),"r") as file:
        history=json.loads(file.read())
        file.close()
    except:
      with open("media/json/history_{}.json".format(username),"w") as file:
        history=json.loads(open("templates/json/history.json").read())
        file.write(json.dumps(history, indent = 4))
        file.close()
    
    if "search" in request.POST.keys():
          return redirect("/documentation?page=elements#"+request.POST['search'])
    elif "type" in request.POST.keys() and request.POST['type'] is not None:
      if request.POST['type'] in ['JSON','PDF']:
            
        if request.POST['type']=="JSON":
              jsonexport=request.POST['data'].replace("'","\"")
              filename = "search_"+request.POST['data'].split(":")[0].replace("'","")+'.json'
              response = HttpResponse(jsonexport,content_type='application/json')
              response['Content-Length'] = len(response.content)
              response['Content-Disposition'] = 'attachment; filename='+str(filename)
              return response
            
        elif request.POST['type']=="PDF":
              jsondata="{"+request.POST['data'][::-1].replace(",","",1)[::-1].replace("'","\"")+"}"
              jsondata=jsondata.replace(">",">\"").replace("<","\"<")
              data=eval(jsondata)
              data['export']=True
              try:
                if "gpsmap" in data["ip"].keys():
                  del data["ip"]["gpsmap"]
              except:
                pass
  
              if "Social" not in data.keys():
                html_string=render(request,"results.html",data).content.decode("utf-8")
              else:
                html_string=render(request,"social.html",data).content.decode("utf-8")
              #print(html_string)
              filename="Search_"+request.POST['data'].split(":")[0].replace("'","")+".pdf"
              
              try:
                disp=Display(backend="xvfb")
                disp.start()
                pdf = pdfkit.PDFKit(html_string, "string").to_pdf()
                disp.stop()
                response = HttpResponse(pdf)
                response['Content-Type'] = 'application/pdf'
                response['Content-disposition'] = 'attachment;filename='
                response['Content-disposition'] += filename
              except:
                html = HTML(string=html_string)
                result = html.write_pdf()
                response = HttpResponse(content_type='application/pdf;')
                response['Content-Disposition'] = 'inline; filename={}'.format(filename)
                response['Content-Transfer-Encoding'] = 'binary'
                with tempfile.NamedTemporaryFile(delete=True) as output:
                    output.write(result)
                    output.flush()
                    output = open(output.name, 'rb')
                    response.write(output.read())
  
              return response
          
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
    ratelimit = user.profile.ratelimit

    query = str(request.POST['query'].replace(" ",""))
    query = query.split(":",1)
    query[0]=query[0].lower()
    

    if not len(query)<2:
      #print(request.POST)
      GOOGLE_RECAPTCHA_SECRET_KEY ="6LdcXqUZAAAAAIvII1yxVf24QoFBOpVXa5HDz7wv" #"6Leh06QZAAAAANIV5Wp1CNVfKZL-2NC717YSxpKD"
      recaptcha_response = request.POST.get('g-recaptcha-response')
      url = 'https://www.google.com/recaptcha/api/siteverify'
      values = {
          'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
          'response': recaptcha_response
        }
      data = urllib.parse.urlencode(values).encode()
      req =  urllib.request.Request(url, data=data)
      response = urllib.request.urlopen(req)
      result = json.loads(response.read().decode())
      #print(result) result['success']
      if True==True:
        if ratelimit>0:
          ratelimit=ratelimit-1
          user.profile.ratelimit=ratelimit
          user.save()
          
          request_type = str(query[0])
          request_data = str(query[1])
          
          with open("media/json/data.json","r") as file:
            data=json.loads(file.read())
            file.close()
          #print(data)
          
          if "ajax" in request.POST.keys() and request.POST["ajax"]=="True":
            history["query_type"][request_type]+=1
            history["notifications"].insert(0,"{} started at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
            with open("media/json/history_{}.json".format(username),"w") as file:
              file.write(json.dumps(history, indent = 4))
          
          if request_type == 'facebook':
            if googlemapapikey is not None or googlemapapikey !="":
              return social(request, request_type, request_data, googlemapapikey)
            else:
              error = 'Missing Google Map API Key'
              return render(request, 'index.html', {'error':error})

          elif request_type == 'twitter':
            if googlemapapikey is not None or googlemapapikey !="":
              return social(request, request_type, request_data, googlemapapikey)
            else:
              error = 'Missing Google Map API Key'
              return render(request, 'index.html', {'error':error})

          elif request_type == 'instagram':
            if googlemapapikey is not None or googlemapapikey !="":
              return social(request, request_type, request_data, googlemapapikey)
            else:
              error = 'Missing Google Map API Key'
              return render(request, 'index.html', {'error':error})    

          elif request_type == 'social':
            if googlemapapikey is not None or googlemapapikey !="":
              return social(request, request_type, request_data, googlemapapikey)
            else:
              error = 'Missing Google Map API Key'
              return render(request, 'index.html', {'error':error})

          elif request_type == 'ip':
            if request_data in data[request_type].keys():
              ip=data[request_type][request_data]
            else:
              ip={}
              
              if ipstackkey is None or ipstackkey =="":
                error = 'Missing Ip Stack API Key'
                return render(request, 'index.html', {'error':error})
              else:
                ipdata=IPtrace(request_data, ipstackkey)
                ip["ipapi"] = ipdata["ipapi"]
                ip['ipstackdata']= ipdata['ipstackdata']
                
              portscandata = DefaultPort(request_data)
              if portscandata['Ports'] :
                ip['portscan']=portscandata

              censysdata = censys_ip(request_data)
              if censysdata :
                ip['censys']=censysdata

              if shodankey is None or shodankey =="":
                error = 'Missing Shodan API Key'
                return render(request, 'index.html', {'error':error})
              else:
                shodandata = shodan_ip(request_data,shodankey)
                if 'Error' not in shodandata.keys():
                  ip['shodan']=shodandata
                
              ip['torrentdata'] = GetTorrent(request_data)
              data[request_type][request_data]=ip
              with open("media/json/data.json","w") as file:
                file.write(json.dumps(data, indent = 4))
              
            lats = ip['ipstackdata']['latitude']
            lons = ip['ipstackdata']['longitude']
            if googlemapapikey is None or googlemapapikey=="":
              error = 'Missing Google Maps API Key'
              return render(request, 'index.html', {'error':error})
            else:
              ip['gmap3']=heat_map([lats],[lons],googlemapapikey)

            if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
              history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
              history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
              with open("media/json/history_{}.json".format(username),"w") as file:
                file.write(json.dumps(history, indent = 4))
              return JsonResponse(history["notifications"],safe=False)
            return render(request, 'results.html',{'ip':ip})
            
          elif request_type == 'victimtrack':

            request_data = request_data.split(',')
            pubip = request_data[0]

            ip={}

            if googlemapapikey is None or googlemapapikey =="":
                error = 'Missing Ip Stack API Key'
                return render(request, 'index.html', {'error':error})
            try:
              if request_data[1].replace('.', '', 1).isdigit() and request_data[2].replace('.', '', 1).isdigit():
                lat = float(request_data[1])
                lon = float(request_data[2])
                ip['gpsmap']=gps_map([lat],[lon],googlemapapikey) #GPS Latitude and Longitude 
            except:
                pass
      
            if ipstackkey is None or ipstackkey=="":
              error = 'Missing Ip Stack API Key'
              return render(request, 'index.html', {'error':error})
            else:
              ip= IPtrace(pubip, ipstackkey)
              ip["ipstackdata"]=ip["ipstackdata"]
              ip["ipapi"]=ip["ipapi"]
              iplats = ip['ipstackdata']['latitude']
              iplons = ip['ipstackdata']['longitude']
            
            #ip['gmap3']=heat_map([iplats],[iplons],googlemapapikey) # IP Stack Latitude & Longitude
            
            return render(request, 'results.html',{'ip':ip,'iplats':iplats,'iplons':iplons})

          elif request_type == 'phone':
            if request_data in data[request_type].keys():
              if "numverify" in data[request_type][request_data].keys():
                numverifydata=data[request_type][request_data]["numverify"]
              
              getcontactdata=data[request_type][request_data]["getcontactdata"]
              hlrdata = data[request_type][request_data]["hlrdata"]
            else:
              if apilayerphone=="" or apilayerphone=="" or hlruname=="" or hlrpwd=="":
                number=request_data.replace("+","")
                numverifydata=numverify(number)
                data[request_type][request_data]={'numverify':numverifydata}
                with open("media/json/data.json","w") as file:
                  file.write(json.dumps(data, indent = 4))
                return render(request,'results.html',{'numverify':numverifydata})
              
              getcontactdata=getcontact(request_data)
              hlrdata = HLRlookup(request_data, apilayerphone, hlruname,hlrpwd)

              data[request_type][request_data]={"getcontactdata":getcontactdata,"hlrdata":hlrdata}
              with open("media/json/data.json","w") as file:
                file.write(json.dumps(data, indent = 4))
            
            if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
              history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
              history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
              with open("media/json/history_{}.json".format(username),"w") as file:
                file.write(json.dumps(history, indent = 4))
              return JsonResponse(history["notifications"],safe=False)
            return render(request, 'results.html',{'hlrdata':hlrdata,'getcontactdata':getcontactdata})

          elif request_type == 'mac':
            if request_data in data[request_type].keys():
              macdata = data[request_type][request_data]["macdata"]
              if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
                history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
                history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
                with open("media/json/history_{}.json".format(username),"w") as file:
                  file.write(json.dumps(history, indent = 4))
                return JsonResponse(history["notifications"],safe=False)
              return render(request, 'results.html',{'macdata':macdata})
            else:
              if len(request_data)==17 and len(request_data.split(":"))==6:
                  if macapikey is None or macapikey =="":
                    error = 'Missing Ip MacVender API Key'
                    return render(request, 'index.html', {'error':error})
                  
                  macdata = macLookup(request_data, macapikey)
                  data[request_type][request_data]={'macdata':macdata}
                  with open("media/json/data.json","w") as file:
                    file.write(json.dumps(data, indent = 4))
                  if 'Error' in macdata.keys():
                      return render(request,'results.html',{'Error':macdata['Error']})
                  else:
                      if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
                        history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
                        history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
                        with open("media/json/history_{}.json".format(username),"w") as file:
                          file.write(json.dumps(history, indent = 4))
                        return JsonResponse(history["notifications"],safe=False)
                      return render(request, 'results.html',{'macdata':macdata})
              else:
                  return render(request,'index.html',{'error':"Invalid Mac Address"})
          
          elif request_type == 'email':
            if request_data in data[request_type].keys():
              hibp=data[request_type][request_data]["hibp"]
              hunterio=data[request_type][request_data]["hunterio"]
              emailrepdata=data[request_type][request_data]["emailrep"]
              ghostdata=data[request_type][request_data]["ghostdata"]
              slideshare=data[request_type][request_data]["slideshare"]
            else:
              if hibpkey is None or hibpkey=="":
                  error = 'Missing HaveIbeenPwned API Key'
                  return render(request, 'index.html', {'error':error})
              else:
                hibp=HaveIbeenPwned(request_data,hibpkey)
              if hunterkey is None or hunterkey=="":
                  error = 'Missing Hunter API Key'
                  return render(request, 'index.html', {'error':error})
              else:
                hunterio=hunter(request_data,hunterkey)
              if emailrepkey is None or emailrepkey=="":
                  error = 'Missing Ip EmailRep Key'
                  return render(request, 'index.html', {'error':error})
              else:
                emailrepdata=emailrep(request_data,emailrepkey)
              ghostdata = ghostproject(request_data)  
              slideshare = SlideShare(request_data)
              data[request_type][request_data]={'hibp':hibp,'hunterio':hunterio,'emailrep':emailrepdata,'ghostdata':ghostdata, 'slideshare':slideshare}
              with open("media/json/data.json","w") as file:
                file.write(json.dumps(data, indent = 4))
            if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
              history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
              history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
              with open("media/json/history_{}.json".format(username),"w") as file:
                file.write(json.dumps(history, indent = 4))
              return JsonResponse(history["notifications"],safe=False)
            return render(request,'results.html',{'hibp':hibp,'hunterio':hunterio,'emailrep':emailrepdata,'ghostdata':ghostdata, 'slideshare':slideshare})
        
          elif request_type == 'domain':
                return domain(request,request_data)

          elif request_type == 'cluster':
            jsonurl = MakeCluster(request,request_data.split(","))
            return render(request, 'cluster.html', {'url':jsonurl})
              
          elif request_type == 'btc':
            if request_data in data[request_type].keys():
              btc=data[request_type][request_data]["btc"]
            else:
              btc=btcaddress(request_data)
              data[request_type][request_data]={'btc':btc}
              with open("media/json/data.json","w") as file:
                file.write(json.dumps(data, indent = 4))
            if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
              history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
              history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
              with open("media/json/history_{}.json".format(username),"w") as file:
                file.write(json.dumps(history, indent = 4))
              return JsonResponse(history["notifications"],safe=False)
            return render(request,'results.html',{'btc':btc})
              
          elif request_type == 'vehicle':
            if request_data in data[request_type].keys():
              vechileinfo = data[request_type][request_data]["vechileinfo"]
            else:
                vechileinfo=vechileno(request_data)
                data[request_type][request_data]={'vechileinfo':vechileinfo}
                with open("media/json/data.json","w") as file:
                  file.write(json.dumps(data, indent = 4))
            if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
              history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
              history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
              with open("media/json/history_{}.json".format(username),"w") as file:
                file.write(json.dumps(history, indent = 4))
              return JsonResponse(history["notifications"],safe=False)
            return render(request,'results.html',{'vechileinfo':vechileinfo})
              
          elif request_type == 'fbsearch':
                keyword=str(request.POST['query'].split(":")[-1])
                fbsearch=FacebookScrapper(keyword,c_user,xs)
                return render(request,'results.html',{'fbsearch':fbsearch})
          else:
            error = 'The requested Query is INVALID'
            return render(request, 'index.html', {'error':error})
        else:
            reset = datetime.now(timezone.utc) - user.profile.resetdate
            if reset.days==1:
                  user.profile.resetdate=datetime.utcnow().strftime('%m-%d %H:%M:')
                  user.profile.resetcount()
                  user.save()
                  return render(request, 'index.html')
            else:
              error = 'Sorry you have Crossed your search limit'
              return render(request, 'index.html', {'error':error}) 
      else:
          error = 'Recaptcha Not solved or you are a Bot'
          return render(request, 'index.html', {'error':error})

def reports(request):
  username = request.user.username
  
  try:
    with open("media/json/history_{}.json".format(username),"r") as file:
      history=json.loads(file.read())
      file.close()
  except:
    with open("media/json/history_{}.json".format(username),"w") as file:
      history=json.loads(open("templates/json/history.json").read())
      file.write(json.dumps(history, indent = 4))
      file.close()
  #print(history)
  if len(history["Search_query"])==0:
    return render(request,"reports.html")
  return render(request,"reports.html",{"search_query":history["Search_query"]})

def domain(request,request_data):
    username = request.user.username
    query = ["domain",request_data]
    try:
      with open("media/json/history_{}.json".format(username),"r") as file:
        history=json.loads(file.read())
        file.close()
    except:
      with open("media/json/history_{}.json".format(username),"w") as file:
        history=json.loads(open("templates/json/history.json").read())
        file.write(json.dumps(history, indent = 4))
        file.close()
    with open("media/json/data.json","r") as file:
      data=json.loads(file.read())
      file.close()
    request_type = "domain"
    if request_data in data[request_type].keys():
      webosint = data[request_type][request_data]["webosint"]
      portscan = data[request_type][request_data]["portscan"]
    else:
        portscan=DefaultPort(request_data)
        webosint=getDomain(request_data)
        data[request_type][request_data]={"webosint":webosint,'portscan':portscan}
        with open("media/json/data.json","w") as file:
          file.write(json.dumps(data, indent = 4))
          
    if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
      history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
      history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
      with open("media/json/history_{}.json".format(username),"w") as file:
        file.write(json.dumps(history, indent = 4))
      return JsonResponse(history["notifications"],safe=False)
    return render(request,'domain.html',{"webosint":webosint,'portscan':portscan})

def social(request, request_type, request_data, googlemapapikey):
  username = request.user.username
  with open("media/json/data.json","r") as file:
    data=json.loads(file.read())
    file.close()

  query = [request_type,request_data]
  try:
    with open("media/json/history_{}.json".format(username),"r") as file:
      history=json.loads(file.read())
      file.close()
  except:
    with open("media/json/history_{}.json".format(username),"w") as file:
      history=json.loads(open("templates/json/history.json").read())
      file.write(json.dumps(history, indent = 4))
      file.close()
  
  request_type = request_type
  request_data = request_data

  if request_type == 'facebook':
    if request_data in data[request_type].keys():
      fbdata = data[request_type][request_data]
    else:
      fbdata = Facebook(request_data)
      data[request_type][request_data]=fbdata
      with open("media/json/data.json","w") as file:
        file.write(json.dumps(data, indent = 4))
    if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
      history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
      history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
      with open("media/json/history_{}.json".format(username),"w") as file:
        file.write(json.dumps(history, indent = 4))
      return JsonResponse(history["notifications"],safe=False)
    return render(request, 'social.html',{'fbdata':fbdata})

  elif request_type == 'instagram':
      if request_data in data[request_type].keys():
        instadata = data[request_type][request_data]
      else:
        instadata = Instagram(request_data)
        data[request_type][request_data]=instadata
        with open("media/json/data.json","w") as file:
          file.write(json.dumps(data, indent = 4))
      
      if 'Location' in instadata.keys() and len(instadata['Location']) >0:
          gmap3=loc(instadata['Location'],googlemapapikey)
      else:
          instadata['Location']=None
          gmap3=None
      if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
        history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
        history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
        with open("media/json/history_{}.json".format(username),"w") as file:
          file.write(json.dumps(history, indent = 4))
        return JsonResponse(history["notifications"],safe=False)
      return render(request, 'social.html',{'instadata':instadata,'gmap3':gmap3})

  elif request_type == 'twitter':
      if request_data in data[request_type].keys():
        twitterdata = data[request_type][request_data]
      else:
        twitterdata = Twitter(request_data)
        data[request_type][request_data]=twitterdata
        with open("media/json/data.json","w") as file:
          file.write(json.dumps(data, indent = 4))
      if 'Error' not in twitterdata:
        if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
          history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
          history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
          with open("media/json/history_{}.json".format(username),"w") as file:
            file.write(json.dumps(history, indent = 4))
          return JsonResponse(history["notifications"],safe=False)
        return render(request, 'social.html',{'twitterdata':twitterdata})
      else:
        twitterdata = {}
        twitterdata['Error']="Profile Not Found"
        return render(request, 'social.html',{'twitterdata':twitterdata})
    
  elif request_type == 'social':
    location=list()
    socialquery = {}
    socialquery['True'] = 1
    if request_data in data[request_type].keys():
        socialdata = data[request_type][request_data]
        fbdata=socialdata["fbdata"]
        instadata=socialdata["instadata"]
        twitterdata=socialdata["twitterdata"]        
        gitdata= socialdata["gitdata"]
        tinderdata= socialdata["tinder"]
        whatname= socialdata["whatname"]
        gravatardata= socialdata["gravatar"]
        if 'Error' in gravatardata:
          gravatardata = None
        tiktokdata= socialdata["tiktok"]
        mediumdata= socialdata["medium"]
        pinterestdata=socialdata["pinterest"]
        keybasedata= socialdata["keybase"]
        
    else:    
      socialdata  = {}

      def fb(request_data):
        socialdata ['fb'] = Facebook(request_data)

      def insta(request_data):
        socialdata['insta'] = Instagram(request_data)

      def twit(request_data):
        socialdata['twitter'] = Twitter(request_data)

      start=time.perf_counter()

      threads = []

      t1 = Thread(target = fb, args=(request_data,))
      threads.append(t1)
      t2 = Thread(target = insta, args=(request_data,))
      threads.append(t2)
      t3 = Thread(target = twit, args=(request_data,))
      threads.append(t3)

      for x in threads:
        x.start()
        time.sleep(1)

      for x in threads:
        x.join()
        
      fbdata = socialdata['fb']
      
      instadata=socialdata['insta']
      
      twitterdata=socialdata['twitter']

      gitdata= gitscrape(request_data)
  
      tinderdata= tinder(request_data)

      whatname= whatismyname(request_data)
      
      gravatardata= gravatar(request_data)
      if 'Error' in gravatardata:
        gravatardata = None
    
      tiktokdata= tiktok(request_data)
    
      mediumdata= medium(request_data)
      
      pinterestdata= pinterest(request_data)

      keybasedata= keybase(request_data)
      
      data[request_type][request_data]={'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata,'gitdata':gitdata,"tinder":tinderdata,"whatname":whatname,'gravatar':gravatardata,
                  'tiktok':tiktokdata,'medium':mediumdata,'pinterest':pinterestdata,'keybase':keybasedata}
      with open("media/json/data.json","w") as file:
        file.write(json.dumps(data, indent = 4))

    if "Current_city" in fbdata.keys() and fbdata["Current_city"] is not None:
          location.append(fbdata["Current_city"])
    if "Home_Town" in fbdata.keys() and fbdata["Home_Town"] is not None:
          location.append(fbdata["Home_Town"])
    
    if 'Error' not in instadata:
        if 'Location' in instadata.keys() and len(instadata['Location'])>0:
            for i in instadata['Location']:
                location.append(i)
    else:
        pass 

    if 'Error' not in twitterdata:
        if 'location' in twitterdata.keys() and twitterdata['location'] !="Not provided by the user":
            location.append(twitterdata["Location"])
        else:
            pass
    else:
        pass
    if len(location)>0:
        gmap3=loc(location, googlemapapikey)
    else:
        gmap3=None
    if "ajax" in request.POST.keys() and request.POST["ajax"] == "True":
      history["Search_query"].insert(0,{"query":":".join(query),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
      history["notifications"].insert(0,"{} ended at {}".format(request_type,datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')))
      with open("media/json/history_{}.json".format(username),"w") as file:
        file.write(json.dumps(history, indent = 4))
      return JsonResponse(history["notifications"],safe=False)
    return render(request, 'social.html',{'fbdata':fbdata,'instadata':instadata,'twitterdata':twitterdata,'gitdata':gitdata,"tinder":tinderdata,"whatname":whatname,'gravatar':gravatardata,
                  'tiktok':tiktokdata,'medium':mediumdata,'pinterest':pinterestdata,'keybase':keybasedata,
                    'socialquery':socialquery,'gmap3':gmap3})
  else:
    error = 'The requested Query is INVALID'
    return render(request, 'index.html', {'error':error})

def reverseimage(request):
  if request.method=="GET":
    return render(request, 'apps/reverseimage.html')

  elif request.method=="POST":

    if 'input-b2' in request.FILES.keys():
        if request.FILES['input-b2'] != "":
            url=reverseImg(str(request.FILES['input-b2']),request.FILES['input-b2'].file)
            if "https" in url:
                return redirect(url)
            else:
                return render(request, 'apps/reverseimage.html',{"Error":url})
        else:
            return render(request, 'apps/reverseimage.html',{"Error":"Do Select the File"})

def metadata(request):
  username = request.user.username
  user = User.objects.filter(username=username).first()
  
  try:
      with open("media/json/history_{}.json".format(username),"r") as file:
        history=json.loads(file.read())
        file.close()
  except:
    with open("media/json/history_{}.json".format(username),"w") as file:
      history=json.loads(open("templates/json/history.json").read())
      file.write(json.dumps(history, indent = 4))
      file.close()
  
  if request.method=="GET":
  
    return render(request, 'apps/metadata.html',{"GET":'get',"history":history["app_type"]["metadata"][:10]})

  elif request.method=="POST":
      
    if 'metaimage' in request.FILES.keys() or "filename" in request.POST.keys():
        if request.POST.get("filename")!="" or request.FILES['metaimage'] != '' :
            try:
              filename=str(request.FILES['metaimage']).split('.',1)
            except:
              filename=request.POST["filename"].split('.',1)

            if len(filename)==2:
                if filename[-1] in ['jpg','png','gif','tif','jpeg']:
                  try:
                    with open("media/metadata/{}.json".format(username),"r") as file:
                      metafiles = json.loads(file.read())
                  except:
                    with open("media/metadata/{}.json".format(username),"w") as file:
                      metafiles={}
                      file.write(json.dumps({}))
                  filename = ".".join(filename)
                  
                  if 'metaimage' in request.FILES.keys() and str(request.FILES['metaimage']) in metafiles.keys():
                    metadata=metafiles[str(request.FILES['metaimage'])]
                  elif "filename" in request.POST.keys() and filename in metafiles.keys():
                    metadata=metafiles[str(filename)]
                  else:
                    user.profile.metaimage = request.FILES['metaimage']
                    user.profile.save()
                    history["app_type"]["metadata"].insert(0,{"filename":str(request.FILES['metaimage']),"time":datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M %d %b')})
                    with open("media/json/history_{}.json".format(username),"w") as file:
                      file.write(json.dumps(history, indent = 4))
                    metaimage = user.profile.metaimage.url
                    googlemapapikey = user.profile.googlemapapikey
                    metadata = get_exif(metaimage)
                    for i in metadata.keys():
                      try:
                        metadata[i]=str(str(metadata[i],"latin-1").replace("<"," ").replace(">"," "))
                      except:
                        pass
                    os.remove(BASE_DIR + user.profile.metaimage.url)
                    metafiles[str(request.FILES['metaimage'])]=metadata

                    with open("media/metadata/{}.json".format(username),"w") as file:
                      file.write(json.dumps(metafiles))
                    
                  if 'Error' in metadata.keys():
                      return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post","history":history["app_type"]["metadata"][:10]})
                  elif 'Latitude' in metadata.keys():
                        
                      lats = metadata['Latitude']
                      lons = metadata['Longitude']
                      gmap3=heat_map([lats],[lons], googlemapapikey)
                      return render(request, 'apps/metadata.html',{'metadata':metadata, 'gmap3':gmap3, "POST":"post","history":history["app_type"]["metadata"][:10]})
                  else:
                      return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post","history":history["app_type"]["metadata"][:10]})
                elif filename[-1] == 'pdf':
                    user.profile.metaimage = request.FILES['metaimage']
                    user.profile.save()
                    pdf=pdfx.PDFx(BASE_DIR + user.profile.metaimage.url)
                    os.remove(BASE_DIR + user.profile.metaimage.url)
                    metadata=pdf.get_metadata()
                    metadata['references_dict'] = pdf.get_references_as_dict()
                    return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post","history":history["app_type"]["metadata"][:10]})
                else:
                    return render(request, 'apps/metadata.html',{"Error":"Upload a filename with Valid Extension"})
            else:
                return render(request, 'apps/metadata.html',{"Error":"Select Module and File Properly"})
        else:
            return render(request, 'apps/metadata.html',{"Error":"Something Went Wrong"})

def modules(request):
    if request.method=="GET":
        
      return render(request, 'modules.html')
    elif request.method=="POST":
        
        username = request.user.username
        user = User.objects.filter(username=username).first()
        
        if 'metaimage' in request.FILES.keys():
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
                            return render(request, 'results.html',{'metadata':metadata, 'gmap3':gmap3, 'post':post})
                        else:
                            return render(request, 'results.html',{'metadata':metadata, 'post':post})
                    elif filename[-1] == 'pdf':
                        user.profile.metaimage = request.FILES['metaimage']
                        user.profile.save()
                        pdf=pdfx.PDFx(BASE_DIR + user.profile.metaimage.url)
                        os.remove(BASE_DIR + user.profile.metaimage.url)
                        metadata=pdf.get_metadata()
                        metadata['references_dict'] = pdf.get_references_as_dict()
                        return render(request, 'results.html',{'metadata':metadata, 'post':post})
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
              user.profile.hunterkey=jsoncontent['hunterkey']
              
            elif 'apilayerphone' == keys:
              user.profile.apilayerphone = jsoncontent['apilayerphone']

            elif 'hlruname' == keys:
              user.profile.hlruname = jsoncontent['hlruname']

            elif 'hlrpwd' == keys:
              user.profile.hlrpwd = jsoncontent['hlrpwd']
              
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
def receivetrack(request,template,username):
  secret=str(str(request.META['PATH_INFO']).split('/')[-1]).replace('a','=')
  secret=base64.b64decode(secret)
  secret=secret.decode('ascii')
  secret="".join(["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c)+23)%36] for c in secret])
  
  if request.method == 'GET':
    return render(request, request.META['PATH_INFO'].split('/')[1]+'.html')

  elif request.method == 'POST':
    localip = str(request.POST.get('locip'))
    viclatitude = str(request.POST.get('latitude'))
    viclongitude = str(request.POST.get('longitude'))

    vicuseragent = str(request.user_agent.browser.family)

    publicip = str(request.META.get('HTTP_X_REAL_IP'))

    user = User.objects.filter(username=secret).first()

    if user.profile.victimpublicip == '' : # Assigning values for the first time
      user.profile.victimpublicip = publicip
      user.profile.victimlocip = localip
      user.profile.victimlatitude = viclatitude
      user.profile.victimlongitude = viclongitude
      user.profile.victimuseragent = vicuseragent

    elif publicip not in user.profile.victimpublicip or localip not in user.profile.victimlocip:

      if publicip not in user.profile.victimpublicip: #Checking whether the Public Ip already exists in DB
        user.profile.victimpublicip += ','+publicip # Appending values from 2nd time
        user.profile.victimlocip += ','+localip
        user.profile.victimlatitude += ','+viclatitude
        user.profile.victimlongitude += ','+viclongitude
        user.profile.victimuseragent += ','+vicuseragent

      else:
        pass

    user.profile.save()
    return render(request, request.META['PATH_INFO'].split('/')[1]+'.html')

def tracker(request):

  if request.method == 'GET':

    username = request.user.username
    user = User.objects.filter(username=username).first()
    
    secret="".join(["0123456789abcdefghijklmnopqrstuvwxyz"[("0123456789abcdefghijklmnopqrstuvwxyz".find(c)+13)%36] for c in str(username)])
    secret=base64.b64encode(str(secret).encode('ascii'))
    if "=" in str(secret.decode('ascii')):
          secret=str(secret.decode('ascii')).replace('=','a')
    try:
      secret=secret.decode('ascii')
    except:
      pass
    url = {}

    url['1'] = "https://osint.studio/amazonprimegenerator/" + str(secret)

    url['2'] = "https://osint.studio/netflixaccountgenerator/" + str(secret)
  

    # Fetching values from DB as list
    
    victimpublicip = user.profile.victimpublicip
    victimpublicip = victimpublicip.split(",")
    
    victimlocip = user.profile.victimlocip
    victimlocip = victimlocip.split(",")

    viclatitude = user.profile.victimlatitude
    viclatitude = viclatitude.split(",")

    viclongitude = user.profile.victimlongitude
    viclongitude = viclongitude.split(",")

    vicuseragent = user.profile.victimuseragent
    vicuseragent = vicuseragent.split(",")
    
    victim=[]
    for i in range(len(viclatitude)):
      victim.append([victimpublicip[i],victimlocip[i],vicuseragent[i],viclatitude[i],viclongitude[i]])

    if victimpublicip != ['']:
      return render(request, 'apps/tracker.html', {'victim':victim,'url':url})
    else:
      return render(request, 'apps/tracker.html', {'url':url})



  if request.method == 'POST':
    username = request.user.username
    user = User.objects.filter(username=username).first()
    try:
      if request.POST['flush'] == "Confirm":
        user.profile.victimlatitude=""
        user.profile.victimlocip=""
        user.profile.victimpublicip=""
        user.profile.victimlongitude=""
        user.profile.victimuseragent = ""
        user.save()
        return redirect("apps/tracker")
      else:
        pass
    except:
      pass
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
    return render(request, 'change_password.html', {
        'form': form
    })

def logout(request):

  auth.logout(request)
  return HttpResponseRedirect("login")

def login(request):

  if request.method == 'GET':
   return render(request, 'login.html')

  if request.method == 'POST':
    
    GOOGLE_RECAPTCHA_SECRET_KEY ="6LdcXqUZAAAAAIvII1yxVf24QoFBOpVXa5HDz7wv" #"6Leh06QZAAAAANIV5Wp1CNVfKZL-2NC717YSxpKD"
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
          'secret': GOOGLE_RECAPTCHA_SECRET_KEY,
          'response': recaptcha_response
        }
    data = urllib.parse.urlencode(values).encode()
    req =  urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())
    
    if result['success']==True:
      text = request.POST['policeid']

      password = request.POST['password']

      user = auth.authenticate(username=text, password=password)

      if user is not None:
        auth.login(request, user)
        #return render(request, 'dashboard.html', {'user':text})
        return redirect('index')
      else:
        return render(request, 'login.html', {'Auth':'False'})
      
    else:
        return render(request, 'login.html', {'Error':'True'})

def media(request,username):
    #print(request.COOKIES['sessionid'])
    session = Session.objects.get(session_key=request.COOKIES['sessionid'])
    uid = session.get_decoded().get('_auth_user_id')
    user = User.objects.get(pk=uid)
    if user.username==re.findall("/media/json/(.*).json",request.META['PATH_INFO'])[0]:
      with open("media/json/{}.json".format(user.username)) as data:
        jsondata=json.load(data)
        #print(jsondata)
        data.close()
        return JsonResponse(jsondata, safe=False)
    else:
      return forbidden(request,PermissionDenied())

def bad_request_error(request,exception):
  return render(request, 'Error400.html',status=400) 
  
def forbidden(request,exception):
  return render(request, 'Error403.html',status=403) 
  
def page_not_found(request,exception):
  return render(request, 'Error404.html', status=404)
  
def server_error(request):
  return render(request, 'Error500.html', status=500)
