import webbrowser
from PIL import Image
from PIL.ExifTags import TAGS
from django.contrib.auth.models import User, auth
import os
from GPSPhoto import gpsphoto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def get_exif(metaimage):

    try:

        metadata = {}
        metaimage = BASE_DIR + metaimage
        data = gpsphoto.getGPSData(metaimage)
        i = Image.open(metaimage)
        info = i.getexif()
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

    except FileNotFoundError:
        error = {'Error':'File Not Found'}
        metadata = {}
        metadata.update(error)
        return metadata

    # maps_url = "https://maps.google.com/maps?q=%s,+%s" % (lat, lon)
  
