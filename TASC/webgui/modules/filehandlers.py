
import json 

def ReadCentralQueries():

		datafile = open("media/json/data.json","r")
		data= json.loads(datafile.read())
		datafile.close()

		return data

def ReadCentralData(request,mode="r",data=None):

		request_type = request.POST['request_type']
		request_data = request.POST['request_data']

		datafile = open("media/json/data.json",mode)
		loadeddata= json.loads(datafile.read())
		datafile.close()

		if mode=="w":
			data=loadeddata[request_type][request_data]
			datafile.write(json.dumps(data,intend=4))

		return loadeddata[request_type][request_data]

def HistoryData(filename,mode,data=None):

		file = open(filename,mode)
		if data!=None:
			file.write(data)
		else:
			data=file.read()
		return json.loads(data)
