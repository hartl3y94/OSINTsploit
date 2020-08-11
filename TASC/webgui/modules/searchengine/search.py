from .search_engines import Google
from .search_engines.engines import search_engines_dict
from .search_engines.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
from .search_engines import config
from googleapiclient.discovery import build
import re
import json

def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	return res

def searchscrape(name):
	my_api_key = 'AIzaSyAKGik6Fok3_mbIsgquaAnDGNy-h_AjhVw'
	my_cse_id = "005553992128112222999:w1eonxpepby"
	data={
		"aliases":[],
		"username":[],
		"links":[]
	}

	result = google_search(name, my_api_key, my_cse_id)
	regexs = json.loads(open("./webgui/modules/searchengine/regexs.json","r").read())

	for i in result['items']:
		temp=i['displayLink'].split(".")
		if len(temp)>2:
			domain=temp[1]
		else:
			domain=temp[0]
		
		try:
			data['username'].append(re.findall(regexs[domain]['user']['regex'],i['link'])[0])
		except:
			for j in i['link'].split("/")[::-1]:
				temp = re.findall("^(?=[a-zA-Z0-9.-_]{8,20}$)(?!.*[_.]{2})[^-_.].*[^-_.].*[-]*.*$",j.split("?")[0])
				try:
					if temp!=[] or temp[0]!="":
						data['username'].append(temp[0])
						break
					else:
						temp = re.findall("^[a-zA-Z0-9]+([a-zA-Z0-9][a-zA-Z0-9])*[a-zA-Z0-9].*$",j.split("?")[0])
						if temp!=[] or temp!="" or temp[0]!="":
							data['username'].append(temp)
							break
				except:
					break
		try:
			data["aliases"].append(re.findall("<b>(.*?)<\/b>",i['htmlFormattedUrl'])[0])
		except:
			try:
				data["aliases"].append(re.findall("<b>(.*?)<\/b>",i['htmlTitle'])[0])
			except:
				pass

		data["links"].append(i['link'])

	data['aliases']=set(data['aliases'])
	data['username']=set(data['username'])

	engine = AllSearchEngines()
	results = engine.search('filetype:xls OR filetype:txt OR filetype:pdf OR filetype:ppt OR filetype:docx intext:"'+name+'"', 3)
	data['files'] = [[i.split("/")[2],i] for i in results.links()]

	return data

#print(searchscrape("Aravindha Hariharan M"))