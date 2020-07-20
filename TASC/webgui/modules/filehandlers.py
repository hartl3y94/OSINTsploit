
import json 

def ReadCentralQueries():

    datafile = open("media/json/data.json","r")
    data= json.loads(datafile.read())
    datafile.close()

    return data

def ReadCentralData(request):

    request_type = request.POST['request_type']
    request_data = request.POST['request_data']

    datafile = open("media/json/data.json","r")
    loadeddata= json.loads(datafile.read())
    datafile.close()

    data = loadeddata[request_type][request_data]

    return data


