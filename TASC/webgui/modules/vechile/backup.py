import requests
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib.request
import json
import warnings
warnings.simplefilter("ignore", UserWarning)

def platenumber(VinNo):
	s=requests.session()

	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.5',
		'Referer': 'https://www.quora.com/How-do-I-get-the-owner-of-the-vehicle-by-the-registration-number-with-the-API-for-my-app',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
	}


	response=s.get("https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml",headers=headers,verify=False)

	#form_rcdl:j_idt34:j_idt41
	soup=BeautifulSoup(response.content,'html.parser')
	captcha=soup.select("div#capatcha")[0]
	try:
		captcha=str(captcha.find("label").extract().text)
		captcha=" ".join(captcha.split())
		captcha=captcha.replace("=","").rstrip()
		#print(captcha,len(captcha))
		if "lesser" in captcha:
			temp=captcha.split(" ")
			if int(temp[-3])>int(temp[-1]):
				value=temp[-1]
			else:
				value=temp[-3]
		elif "greater" in captcha:
			temp=captcha.split(" ")
			if int(temp[-3])<int(temp[-1]):
				value=temp[-1]
			else:
				value=temp[-3]
		else:
			temp="".join(captcha.split(" "))
			value=eval(temp)
		#print(value)
	except:
		exit()
	jsessionid=response.cookies.get_dict()['JSESSIONID']
	
	soup=BeautifulSoup(response.content,'html.parser')
	soup=soup.find(id="j_id1:javax.faces.ViewState:0",attrs={"name":"javax.faces.ViewState"})
	javaxface=soup.get('value')
	
	soup=BeautifulSoup(response.content,'html.parser')
	soup=soup.find("button", attrs={ "class" : "ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only" })
	buttonid=soup['id']
	
	cookies = {
		'JSESSIONID': str(jsessionid),
    	'SERVERID_7081': 'vahanapi_7082',
    	'SERVERID_7082': 'nrservice_7082',
	}
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
		'Accept': 'application/xml, text/xml, */*; q=0.01',
		'Accept-Language': 'en-US,en;q=0.5',
		'Referer': 'https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'Faces-Request': 'partial/ajax',
		'X-Requested-With': 'XMLHttpRequest',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
	}

	data = {
	  'javax.faces.partial.ajax': 'true',
	  'javax.faces.source': str(buttonid),
	  'javax.faces.partial.execute': '@all',
	  'javax.faces.partial.render': 'rcDetailsPanel resultPanel userMessages capatcha txt_ALPHA_NUMERIC',
	   str(buttonid): str(buttonid),
	  'masterLayout': 'masterLayout',
	  'regn_no1_exact': str(VinNo),
	  'txt_ALPHA_NUMERIC': "{}".format(value),
	  'javax.faces.ViewState': str(javaxface),
	}
	
	response = requests.post('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml', headers=headers, cookies=cookies, data=data,verify=False)
	soup = BeautifulSoup(response.content)
	
	if "Vehicle Detail not found" in str(soup):
		return {"Error":"Invalid Plate Numeber or Vehicle Detail not found"}
	elif "<error>" not in str(soup):
		soup.select("div#row")
		table = soup.find('div')
		try:
			data=table.extract().text.split("\n")
			for i in range(len(data)):
				data[i]=data[i].strip()
			data.remove("Vehicle Details Showing in Registering Authority")

			while("" in data) : 
				data.remove("")
			temp=data[0][3:].split(":")
			data[0]=temp[1].strip()
			data.insert(0,temp[0])
			info={}
			for i in range(0,len(data)-1,2):
				if ":" in data[i]:
					data[i]=data[i].replace(":","")
				if ":" in data[i+1]:
					data[i+1]=data[i+1].replace(":","")
				info[data[i]]=data[i+1]
			return info
		except:
			return {"Error":"Something Went Wrong"}
	else:
		return {"Error":"Something Went Wrong"}

def vechileno(number):	
	number.upper()
	data=platenumber(number)
	while "Error" in data.keys() and data["Error"]=="Something Went Wrong":
		data=platenumber(number)
	return data
	