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
def common_social(udata):
    location=list()
    data = {}

    def fb(request_data):
        data['fb'] = Facebook(request_data)

    def twit(request_data):
        data['twitter'] = Twitter(request_data)

    def link(request_data):
        data['linkedin'] = linkedin(request_data)

    threads = []
    if "facebook" in udata.keys():
        t1 = Thread(target = fb, args=(udata['facebook'],))
        threads.append(t1)
    if "twitter" in udata.keys():
        t3 = Thread(target = twit, args=(udata['twitter'],))
        threads.append(t3)
    if "linkedin" in udata.keys():
        t4 = Thread(target = link, args=(udata['linkedin'],))
        threads.append(t4)

    for x in threads:
        x.start()
        time.sleep(1)

    for x in threads:
        x.join()

    commonsocial = {}
    if "fb" in data.keys():
        fbdata = data['fb']
        if "Current_city" in fbdata.keys() is not None:
            location.append(fbdata["Current_city"])
        if "Home_Town" in fbdata.keys() is not None:
            location.append(fbdata["Home_Town"])
        commonsocial['fbdata'] = fbdata
    
    if "instagram" in udata.keys():
        instadata=Instagram(udata['instagram'])
        if 'Error' not in instadata:
            if 'Location' in instadata.keys() and len(instadata['Location'])>0:
                for i in instadata['Location']:
                    location.append(i)
        commonsocial['instadata'] = instadata

    if "twitter" in data.keys():
        twitterdata=data['twitter']
        if 'Error' not in twitterdata:
            if twitterdata['Location'] !="Not provided by the user":
                location.append(twitterdata["Location"])
        commonsocial['twitterdata'] = twitterdata

    if "linkedin" in data.keys():
        linkedindata=data['linkedin']
        commonsocial['linkedin'] = linkedindata
    
    commonsocial['location'] = location # Location from Facebook, Twitter and Instagram together as List
    return commonsocial    

def Social(request, request_type, request_data):
    
    social = {}
    def what(request_data):
        social['whatname']= whatismyname(request_data)

    t1 = Thread(target = what, args=(request_data,))

    t1.start()
    time.sleep(1)

    t1.join()

    social['github'] = gitscrape(request_data)
    social['tinder'] = tinder(request_data)
    social['gravatar'] = gravatar(request_data)
    social['tiktok'] = tiktok(request_data)
    social['medium'] = medium(request_data)
    social['pinterest'] = pinterest(request_data)
    social['keybase'] = keybase(request_data)
    social['reddit'] = reddit(request_data)
    social['telegram'] = telegram(request_data)

    return social
