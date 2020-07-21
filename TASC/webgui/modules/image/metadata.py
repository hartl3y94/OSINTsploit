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
def MetaPdf(request,url):
    pdf=pdfx.PDFx(BASE_DIR + url)
    os.remove(BASE_DIR + url)
    metadata=pdf.get_metadata()
    if pdf.get_references_as_dict() != {}:
        metadata['references_dict'] = pdf.get_references_as_dict()
    return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})
    
def Metadata(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    user.profile.metaimage = request.FILES['metaimage']
    user.profile.save()
    googlemapapikey = user.profile.googlemapapikey
    filename=str(request.FILES['metaimage']).split('.',1)

    if filename[-1] in ['jpg','png','gif','tif','jpeg']:

        metadata = get_exif(user.profile.metaimage.url)

        if 'Error' in metadata.keys():
            return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})

        elif 'Latitude' in metadata.keys():

            lats = metadata['Latitude']
            lons = metadata['Longitude']
            gmap3=heat_map([lats],[lons], googlemapapikey)
            return render(request, 'apps/metadata.html',{'metadata':metadata, 'gmap3':gmap3, "POST":"post"})

        else:
            return render(request, 'apps/metadata.html',{'metadata':metadata, "POST":"post"})

    elif filename[-1] == 'pdf':
        return MetaPdf(request,user.profile.metaimage.url)
    else:
        return render(request, 'apps/metadata.html',{"Error":"Upload a filename with Valid Extension"})

    