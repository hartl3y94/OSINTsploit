
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

import json
from .social.locmap import loc, heat_map, gps_map
from datetime import datetime, timezone
from dateutil import tz

def ReadCentralQueries(request_type):

	datafile = open("media/json/data/{}.json".format(request_type),"r")
	data= json.loads(datafile.read())
	datafile.close()

	return data

def endtimeupdate(request):
	username = request.user.username
	user = User.objects.filter(username=username).first()
	request_type = request.POST['query'].split(":",1)[0]
	request_data = request.POST['query'].split(":",1)[1]
	try:
		history = HistoryData("media/json/history_{}.json".format(username),"r")
	except FileNotFoundError:
		history = HistoryData("media/json/history_{}.json".format(username),"w",open("templates/json/history.json").read())
	endtime = datetime.now().astimezone(tz.gettz('ITC')).strftime('%H:%M') # Scan End Time

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

	request_type = request.POST['query'].split(":",1)[0]
	request_data = request.POST['query'].split(":",1)[1]

	
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
		endtimeupdate(request)		
		datafile.write(json.dumps(loadeddata,indent=4))

	elif request_type == "social":
		social = loadeddata[request_type][request_data]
		if googlemapapikey != "":
			if "location" in social.keys():
				location=social['location']
				gmap3=loc(location, googlemapapikey)
			else:
				gmap3=None
		else:

			return render(request, 'index.html', {'Error': 'Missing Google Map API Key'})
		return render(request, 'viewreports/social.html',{'social':social,'gmap3':gmap3})

	elif request_type == "ip":
		ip=loadeddata[request_type][request_data]
		lats = ip['ipstackdata']['latitude']
		lons = ip['ipstackdata']['longitude']
		ip['gmap3'] = heat_map([lats], [lons], googlemapapikey)
		return render(request, 'viewreports/ip.html', {'ip': ip})

	elif request_type == "phone":
		phone = loadeddata[request_type][request_data]
		getcontactdata = phone['getcontactdata']
		hlrdata = phone['hlrdata']
		numverify = phone['numverify']
		return render(request, 'viewreports/phone.html', {'getcontactdata':getcontactdata, 'hlrdata':hlrdata, 'numverify':numverify})

	elif request_type == "mac":
		macdata = loadeddata[request_type][request_data]
		if 'Error' in macdata.keys():
			return render(request, 'viewreports/mac.html', {'Error': macdata['Error']})
		else:
			return render(request, 'viewreports/mac.html', {'macdata': macdata})

	elif request_type == "email":
		email = loadeddata[request_type][request_data]
		hibp = email['hibp']
		emailrep = email['emailrep']
		hunterio = email['hunterio']
		ghostdata = email['ghostdata']
		return render(request, 'viewreports/email.html', {'hibp':hibp,'emailrep':emailrep, 'hunterio':hunterio, 'ghostdata':ghostdata})

	elif request_type == "domain":
		webosint = loadeddata[request_type][request_data]["webosint"]
		portscan = loadeddata[request_type][request_data]["portscan"]
		return render(request, 'viewreports/domain.html', {"webosint": webosint, 'portscan': portscan})

	elif request_type == "btc":
		btc = loadeddata[request_type][request_data]
		return render(request, 'viewreports/btc.html', {'btc': btc})

	elif request_type == "vehicle":
		vechileinfo = loadeddata[request_type][request_data]
		return render(request, 'viewreports/vehicle.html', {'vechileinfo': vechileinfo})

def HistoryData(filename,mode,data=None):

	file = open(filename,mode)
	if data!=None:
		file.write(data)
	else:
		data=file.read()
	return json.loads(data)
