from .facebook import Facebook
from .instagram import Instagram
from .twitter import Twitter
from .linkedin import linkedin
from .tinder import tinder
from .accounts import whatismyname
from .tiktok import tiktok
from .gravatar import gravatar
from .medium import medium
from .pinterest import pinterest
from .keybase import keybase
from .gitscrape import gitscrape
from .reddit import reddit
from ..searchengine.search import searchscrape
from .telegram import telegram
from threading import Thread
import time

def Social(request, request_type, request_data):

    location=list()
    socialquery = {}
    socialquery['True'] = 1

    data = {}

    def fb(request_data):
        data['fb'] = Facebook(request_data)

    def insta(request_data):
        data['insta'] = Instagram(request_data)

    def twit(request_data):
        data['twitter'] = Twitter(request_data)

    def link(request_data):
        data['linkedin'] = linkedin(request_data)

    threads = []

    t1 = Thread(target = fb, args=(request_data,))
    threads.append(t1)
    t2 = Thread(target = insta, args=(request_data,))
    threads.append(t2)
    t3 = Thread(target = twit, args=(request_data,))
    threads.append(t3)
    t4 = Thread(target = link, args=(request_data,))
    threads.append(t4)

    for x in threads:
        x.start()
        time.sleep(1)

    for x in threads:
        x.join()

    fbdata = data['fb']
    if "Current_city" in fbdata.keys() is not None:
        location.append(fbdata["Current_city"])
    if "Home_Town" in fbdata.keys() is not None:
        location.append(fbdata["Home_Town"])
    
    
    instadata=data['insta']
    if 'Error' not in instadata:
        if 'Location' in instadata.keys() and len(instadata['Location'])>0:
            for i in instadata['Location']:
                location.append(i)


    twitterdata=data['twitter']
    if 'Error' not in twitterdata:
        if twitterdata['Location'] !="Not provided by the user":
            location.append(twitterdata["Location"])

    linkedindata=data['linkedin']
    
    social = {}

    social['github'] = gitscrape(request_data)
    social['tinder'] = tinder(request_data)
    social['whatname'] = whatismyname(request_data)
    social['gravatar'] = gravatar(request_data)
    social['tiktok'] = tiktok(request_data)
    social['medium'] = medium(request_data)
    social['pinterest'] = pinterest(request_data)
    social['keybase'] = keybase(request_data)
    social['reddit'] = reddit(request_data)
    social['fbdata'] = fbdata
    social['instadata'] = instadata
    social['twitterdata'] = twitterdata
    social['linkedin'] = linkedindata
    social['telegram'] = telegram(request_data)
    social['search'] = searchscrape(request_data)

    social['location'] = location # Location from Facebook, Twitter and Instagram together as List
    
    return social