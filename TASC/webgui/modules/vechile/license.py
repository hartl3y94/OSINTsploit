import requests
from bs4 import BeautifulSoup
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib.request
import json
import warnings
warnings.simplefilter("ignore", UserWarning)
from selenium import webdriver
from PIL import Image
from io import BytesIO
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


def platenumber(VinNo):
	options = Options()
	options.headless = True
	fox = webdriver.Firefox(options=options)
	while True:
		fox.get('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml')
		if "not available" in fox.page_source:
			fox.get('https://vahan.nic.in/nrservices/faces/user/searchstatus.xhtml')		

		# now that we have the preliminary stuff out of the way time to get that image :D
		element = fox.find_element_by_id('capatcha') # find part of the page you want image of
		location = element.location
		size = element.size
		png = fox.get_screenshot_as_png() # saves screenshot of entire page


		im = Image.open(BytesIO(png)) # uses PIL library to open image in memory

		left = location['x']
		top = location['y']
		right = location['x'] + size['width']
		bottom = location['y'] + size['height']


		im = im.crop((left, top, right, bottom)) # defines crop points
		im.save('screenshot.png') # saves new cropped image

		#resp=requests.get("https://api.ocr.space/parse/imageurl?apikey=cccfda712e88957&url="+url+"&language=eng")
		#print(resp.text)
		payload = {'apikey': "cccfda712e88957",'language': "eng",}
		with open("screenshot.png",'rb') as f:
			r = requests.post('https://api.ocr.space/parse/image',files={"screenshot.png": f},data=payload)
		resp=json.loads(r.content.decode())
		#print(resp)
		captcha=resp["ParsedResults"][0]['ParsedText']
		if captcha=="":
			continue
		try:
			captcha=" ".join(captcha.split())
			captcha=captcha.replace("\\r\\n"," ").replace("=","").rstrip()
			#print(captcha)
			if "lesser" in captcha:
				temp=captcha.split(" ")
				if temp[-2]!=",":
					temp1=temp[:-1]
					temp1.append(",")
					temp1.append(temp[-1])
					temp=temp1
				#print(temp)
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
			if value!=None:
				break
			else:
				continue
		except:
			continue
	fox.find_element_by_id("regn_no1_exact").send_keys(VinNo)
	time.sleep(1)
	fox.find_element_by_id("txt_ALPHA_NUMERIC").send_keys(value)
	fox.find_element_by_id("txt_ALPHA_NUMERIC").send_keys(Keys.RETURN)
	time.sleep(2)
	soup=BeautifulSoup(fox.page_source)
	time.sleep(3)
	fox.quit()
	if "Vehicle Detail not found" in str(soup):
		return {"Error":"Invalid Plate Numeber or Vehicle Detail not found"}
	elif "<error>" not in str(soup):
		soup=soup.find("div", {"id": "rcDetailsPanel"})
		try:
			table = soup.find_all("div", {"class": "row"})
		except:
			return {"Error":"Invalid Vehicle Number or Not Found"}
		table=table[1:-1]
		try:
			data=list()
			for i in table:
				data.append(i.extract().text.strip())
			#print(data)
			for i in range(len(data)):
				data[i]=data[i].split("\n")
				for j in data[i]:
					if j !="":
						data[i][data[i].index(j)]=j.strip()
				while ("" in data[i]):
					data[i].remove("")

			temp=[j for i in data for j in i]
			data=temp
			info={}
			temp=temp[0].split(".")[1].split(":")
			info[temp[0]]=temp[1]
			
			for i in range(1,len(data),2):
				info[data[i].split(":")[0]]=data[i+1]
			return info
		except:
			return {"Error":"Something Went Wrong"}
	else:
		return {"Error":"Something Went Wrong"}
	
def vechileno(number):	
	number.upper()
	data=platenumber(number)
	return data
	
#print(vechileno("TN36AA8888"))

