import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re

def SlideShare(email):
    req = requests.get('http://www.slideshare.net/search/slideshow?q=%s' % (email))
    soup = BeautifulSoup(req.content, "lxml")
    atag = soup.findAll('a', {'class': 'title title-link antialiased j-slideshow-title'})
    slides = {}
    data = {}
    for at in atag:
        slides[at.text] = at['href']
    
    if len(slides) == 0:
        return None

    else:
        data['length'] = len(slides)
        data['slides'] = {}
        for tl, lnk in slides.items():
            data['slides'][str(tl).strip()] = "http://www.slideshare.net" + str(lnk).strip()
        return data

SlideShare("sebastien.gioria@owasp.org")