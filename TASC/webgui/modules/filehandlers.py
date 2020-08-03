
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

import json
from .social.locmap import loc, heat_map, gps_map
from .ip.multipleip import read_multiple_ip
from datetime import datetime, timezone
from dateutil import tz
import re

def cases(activity):
	file = open("media/json/history.json","r")
	history = json.loads(file.read())
	file.close()
	if activity[0]['caseno'] not in history['cases']:
		history['activity'][activity[0]['caseno']]={"casename":activity[0]['casename'],'query':[]}
		history['cases'].append(activity[0]['caseno'])
		
	history['activity'][activity[0]['caseno']]['query'].insert(0,activity[1:])

	open("media/json/history.json","w").write(json.dumps(history, indent = 4))


	try:
		file=open("media/json/case/"+activity[0]['caseno']+".json","r")
		casedata=json.loads(file.read())
	except:
		casedata=json.loads(open("media/json/casetemplate.json","r").read())
		casedata['name']=activity[0]['casename']
		casedata['no']=activity[0]['caseno']
		casedata['description']=activity[0]['casedescription']
		casedata['team'].append(activity[1])
	casedata['activity'].insert(0,{"query":activity[1:]})
	open("media/json/case/"+activity[0]['caseno']+".json","w").write(json.dumps(casedata,indent=4))

def ReadCentralQueries(request_type):
	try:
		datafile = open("media/json/data/{}.json".format(request_type),"r")
		data= json.loads(datafile.read())
		datafile.close()

		return data
	except:
		return None

def endtimeupdate(request):
	username = request.user.username
	user = User.objects.filter(username=username).first()
	request_type = request.POST['query'].split(":",1)[0]
	request_data = request.POST['query'].split(":",1)[1]
	try:
		history = HistoryData("media/json/history_{}.json".format(username),"r")
	except FileNotFoundError:
		history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())
	endtime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M') # Scan End Time

	for i in history['notifications']:
		if i['Data'] == request_data and i["completed"] == "":
			i['Status']=3
			i['completed']=endtime

	history = HistoryData("media/json/history_{}.json".format(username),"w",json.dumps(history, indent = 4))
	return history
 
def ReadCentralData(request,mode="r",data=None):
	username = request.user.username
	user = User.objects.filter(username=username).first()
	googlemapapikey = user.profile.googlemapapikey
	
	totalquery=[]
	try:
		queries=[request.POST['query']]
	except:
		queries=request.POST['totalquery'].split(",")[1:]
	
	for query in queries:
		request_type = query.split(":",1)[0]
		request_data = query.split(":",1)[1]
		
		datafile = open("media/json/data/{}.json".format(request_type),"r")
		loadeddata= json.loads(datafile.read())
		datafile.close()

		try:
			history = HistoryData("media/json/history_{}.json".format(username),"r")
		except FileNotFoundError:
			history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())
	
		

		if mode=="w":
			datafile = open("media/json/data/{}.json".format(request_type),mode)
			loadeddata[request_type][request_data]=data
			loadeddata[request_type][request_data]['case']=user.profile.case
			endtimeupdate(request)		
			datafile.write(json.dumps(loadeddata,indent=4))

		elif request_type == "social":
			social = loadeddata[request_type][request_data]
			geo=[]
			if googlemapapikey != "":
				if "location" in social.keys():
					location=social['location']
					geo=[lats,lons]=loc(location, googlemapapikey)
					import simplejson
					gmap3=simplejson.dumps(geo)
					
			else:
				return render(request, 'index.html', {'Error': 'Missing Google Map API Key'})
			
			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/social.html',{'social':social,'gmap3':gmap3,'api':googlemapapikey})
			else:
				totalquery.append({request_type:{'social':social,'gmap3':gmap3,'api':googlemapapikey}})

		elif request_type == "ip":
			ip=loadeddata[request_type][request_data]
			lats = ip['ipstackdata']['latitude']
			lons = ip['ipstackdata']['longitude']
			ip['gmap3'] = True #heat_map([lats], [lons], googlemapapikey)

			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/ip.html', {'ip': ip,'api':googlemapapikey})
			else:
				totalquery.append({request_type:{'ip': ip,'api':googlemapapikey}})
			

		elif request_type == "phone":
			phone = loadeddata[request_type][request_data]
			getcontactdata = phone['getcontact']
			hlrdata = phone['hlrlookup']
			numverify = phone['numverify']

			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/phone.html', {'getcontactdata':getcontactdata, 'hlrdata':hlrdata, 'numverify':numverify})
			else:
				totalquery.append({request_type:{'getcontactdata':getcontactdata, 'hlrdata':hlrdata, 'numverify':numverify}})
			

		elif request_type == "mac":
			macdata = loadeddata[request_type][request_data]
			if 'Error' in macdata.keys():
				return render(request, 'viewreports/mac.html', {'Error': macdata['Error']})
			else:
				if 'report' not in request.POST.keys() :
					return render(request, 'viewreports/mac.html', {'macdata': macdata})
				else:
					totalquery.append({request_type:{'macdata': macdata}})
				
		elif request_type == "email":
			email = loadeddata[request_type][request_data]
			hibp = email['hibp']
			emailrep = email['emailrep']
			hunterio = email['hunterio']
			ghostdata = email['ghostdata']

			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/email.html', {'hibp':hibp,'emailrep':emailrep, 'hunterio':hunterio, 'ghostdata':ghostdata})
			else:
				totalquery.append({request_type:{'hibp':hibp,'emailrep':emailrep, 'hunterio':hunterio, 'ghostdata':ghostdata}})
			

		elif request_type == "domain":
			webosint = loadeddata[request_type][request_data]["webosint"]
			portscan = loadeddata[request_type][request_data]["portscan"]
			
			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/domain.html', {"webosint": webosint, 'portscan': portscan})
			else:
				totalquery.append({request_type:{"webosint": webosint, 'portscan': portscan}})
			

		elif request_type == "btc":
			btc = loadeddata[request_type][request_data]

			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/btc.html', {'btc': btc})
			else:
				totalquery.append({request_type:{'btc': btc}})
			

		elif request_type == "vehicle":
			vechileinfo = loadeddata[request_type][request_data]

			if 'report' not in request.POST.keys() :
				return render(request, 'viewreports/vehicle.html', {'vechileinfo': vechileinfo})
			else:
				totalquery.append({request_type:{'vechileinfo': vechileinfo}})
	
	ip=list(set(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",json.dumps(totalquery))))
	gmaps3=read_multiple_ip(ip,user.profile.ipstackkey)
	return render(request,'casereport.html',{"totalquery":totalquery,"heatmap":gmaps3})

def HistoryData(filename,mode,data=None):

	file = open(filename,mode)
	if data!=None:
		file.write(data)
	else:
		data=file.read()
	return json.loads(data)
