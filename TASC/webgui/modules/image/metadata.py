import webbrowser
from PIL import Image
from PIL.ExifTags import TAGS
from django.contrib.auth.models import User, auth
import os
from GPSPhoto import gpsphoto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from xhtml2pdf import pisa
from pyvirtualdisplay import Display
from django.shortcuts import render, redirect
import pdfx, pdfkit, urllib.parse, urllib3, tempfile
from ..social.locmap import loc, heat_map, gps_map
import json
from datetime import datetime, timezone
from dateutil import tz

def get_exif(url): 
    metadata = {}
    metaimage = BASE_DIR + url
    data = gpsphoto.getGPSData(metaimage)
    i = Image.open(metaimage)
    info = i.getexif()
    os.remove(BASE_DIR + url)
    if info == {}:
        error = {'Error':'No Metadata Found'}
        metadata = {}
        metadata.update(error)
        return metadata
    else:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            metadata[decoded] = value

        if "Latitude" in data:

            lat = data['Latitude']
            lon = data['Longitude']
            location = {'Latitude':lat,'Longitude':lon}
            metadata.update(location)

        else:
            pass

        return metadata

    # maps_url = "https://maps.google.com/maps?q=%s,+%s" % (lat, lon)
def MetaPdf(url):
    pdf=pdfx.PDFx(BASE_DIR + url)
    os.remove(BASE_DIR + url)
    metadata=pdf.get_metadata()
    if pdf.get_references_as_dict() != {}:
        metadata['references_dict'] = pdf.get_references_as_dict()
    return metadata
    
def Metadata(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    user.profile.metaimage = request.FILES['metaimage']
    user.profile.save()
    googlemapapikey = user.profile.googlemapapikey
    filename=str(request.FILES['metaimage']).split('.',1)

    try:
        with open("media/metadata/{}.json".format(username),"r") as file:
            metafiles = json.loads(file.read())
    except:
        with open("media/metadata/{}.json".format(username),"w") as file:
            metafiles={}
            file.write(json.dumps(metafiles, indent = 4))
        filename = ".".join(filename)

    history = metafiles
    metadata = {}
    metadata["time"]=datetime.now().astimezone(tz.gettz('ITC')).strftime('%d %B, %Y %H:%M')
    if filename[-1] in ['jpg','png','gif','tif','jpeg']:
        if str(request.FILES['metaimage']) in metafiles.keys():
            metadata['metadata']=metafiles[str(request.FILES['metaimage'])]['metadata']
        else:
            metadata['metadata'] = get_exif(user.profile.metaimage.url)
            
            for i in metadata['metadata'].keys():
                try:
                    metadata['metadata'][i] = str(metadata['metadata'][i])
                    metadata['metadata'][i]= ''.join(e for e in metadata['metadata'][i] if e.isalnum() or e in ['.','-'])
                except Exception as e:
                    pass

            metafiles[str(request.FILES['metaimage'])]=metadata
            with open("media/metadata/{}.json".format(username),"w") as file:
                file.write(json.dumps(metafiles, indent = 4))

        if 'Error' in metadata['metadata'].keys():
            return render(request, 'apps/metadata.html',{'metadata':metadata['metadata'], "POST":"post","history":history})

        elif 'Latitude' in metadata['metadata'].keys():

            lats = float(metadata['metadata']['Latitude'])
            lons = float(metadata['metadata']['Longitude'])
            gmap3=True #heat_map([lats],[lons], googlemapapikey)
            return render(request, 'apps/metadata.html',{'metadata':metadata['metadata'], 'gmap3':gmap3, "POST":"post","history":history,"lats":lats,"lons":lons,"api":googlemapapikey})

        else:
            return render(request, 'apps/metadata.html',{'metadata':metadata['metadata'], "POST":"post","history":history})

    elif filename[-1] == 'pdf':
        if str(request.FILES['metaimage']) in metafiles.keys():
            metadata['metadata']=metafiles[str(request.FILES['metaimage'])]['metadata']
        else:
            metadata['metadata'] = MetaPdf(user.profile.metaimage.url)

            for i in metadata['metadata'].keys():
                try:
                    metadata['metadata'][i]=str(str(metadata['metadata'][i],"latin-1").replace("<"," ").replace(">"," ")).replace("\\","")
                except:
                    pass
            
            metafiles[str(request.FILES['metaimage'])]=metadata
            with open("media/metadata/{}.json".format(username),"w") as file:
                file.write(json.dumps(metafiles, indent = 4))

        return render(request, 'apps/metadata.html',{'metadata':metadata['metadata'], "POST":"post","history":history})
    else:
        return render(request, 'apps/metadata.html',{"Error":"Upload a filename with Valid Extension"})

    