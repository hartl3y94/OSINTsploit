from .search_engines import Google
from .search_engines.engines import search_engines_dict
from .search_engines.multiple_search_engines import MultipleSearchEngines, AllSearchEngines
from .search_engines import config

def searchscrape(name):
	engine = AllSearchEngines("socks5://127.0.0.1:9050",30)

	results = engine.search("{}".format(name),3)
	data = {}
	data['links'] = [[i.split("/")[2],i] for i in results.links()]

	engine = AllSearchEngines()
	results = engine.search('filetype:xls OR filetype:txt OR filetype:pdf OR filetype:ppt OR filetype:docx intext:"'+name+'"', 3)
	data['files'] = [[i.split("/")[2],i] for i in results.links()]

	return data