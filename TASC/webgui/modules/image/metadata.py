import webbrowser
from PIL import Image
from PIL.ExifTags import TAGS
from django.contrib.auth.models import User, auth
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def get_exif(metaimage):

    try:

        metadata = {}
        metaimage = BASE_DIR + metaimage
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

            if "GPSInfo" in metadata:

                lat = [float(x) / float(y) for x, y in metadata['GPSInfo'][2]]
                latref = metadata['GPSInfo'][1]
                lon = [float(x) / float(y) for x, y in metadata['GPSInfo'][4]]
                lonref = metadata['GPSInfo'][3]

                lat = lat[0] + lat[1] / 60 + lat[2] / 3600
                lon = lon[0] + lon[1] / 60 + lon[2] / 3600
                if latref == 'S':
                    lat = -lat
                if lonref == 'W':
                    lon = -lon
                
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
  
