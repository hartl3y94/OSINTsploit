import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import re
from torrequest import TorRequest
import random


'''def Instagram(username):
    
    tr=TorRequest(password='pass')
    tr.reset_identity() #Reset Tor

    proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
    }
    
    session = HTMLSession()

    instadetails={}
    ds_user_id=["38749769686",'39136005627']
    sessionid=['38749769686%3AVUGL0FYS47E1JC%3A20',"6753257913%3AhWD3V3jdQ3Lvoc%3A13"]
    csrftoken=["DwEWoPqRKZXgZPu2Mo6pNSSpOFqhX9zd",'Yy6aOzfm9M0dYi8nv7UG8pZKSp4oXNVl']
    mid=["XwWhPQAEAAFyEV6d4_K9zNopg4",'XwSbUwAEAAHu43GNKoyIPXgOMxJ-']
    urlgen=["{\\\"2409:4072:786:8ea:4cc2:f58c:6859:18ba\\\": 55836}:1jt7UL:4CF6HKT33x7GGUEkTxyIGti0DEQ",'{\\"49.205.147.98\\": 131269}:1jspzg:PBflQh-mhE9IQEbaD17uL2W15dw']
    
    cookies = {
            'csrftoken': random.choices(csrftoken)[0],
            'rur': 'FRC',
            'mid': random.choices(mid)[0],
            'ig_did': '80E8A247-21E6-4DC7-BB85-3CC45C0F4017',
            'ds_user_id': random.choices(ds_user_id)[0],
            'sessionid': random.choices(sessionid)[0],
            'urlgen': random.choices(urlgen)[0],
        }

    headers = {
            '$Host': 'www.instagram.com',
            '$User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
            '$Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            '$Accept-Language': 'en-US,en;q=0.5',
            '$Accept-Encoding': 'gzip, deflate',
            '$Connection': 'close',
            '$Upgrade-Insecure-Requests': '1',
            '$Cache-Control': 'max-age=0',
        }
    try:
        user_name=username
        try:
            temp=2
            while temp>0:
                response = session.get('https://www.instagram.com/'+user_name, headers=headers, cookies=cookies,proxies=proxies)
                soup = BeautifulSoup(response.content, features="lxml")
                l=soup.findAll('script')
                l=l[4].text.split(" = ",1)
                l=l[1][:-1]
                data=json.loads(l)
                #print(data)
                data1=data['entry_data']['ProfilePage']
                if len(data1)>0:
                    break
                temp-=1
        except:
            pass
        data2=data1[0]['graphql']['user']
        url=data2['external_url']
        Name=data2['full_name']
        instadetails["Name"]=Name

    #+++++++++++++++++++Instgram_DP++++++++++++++++++++

        if url is not None:
            instadetails["URL"]=url
        instadetails["Bio"]=str(data2['biography'])

        instadetails["Followers"]=data2['edge_followed_by']['count']

        instadetails["Following"]=data2['edge_follow']['count']

        instadetails["No_of_posts"]=data2['edge_owner_to_timeline_media']['count']

        data3=data2['edge_owner_to_timeline_media']['edges']

        temp=list()
        for i in range(0,len(data3)):
            #print("Image contents: ",content)
            location=data3[i]['node']['location']
            if location is not None:
                #print("Location: ",location['name'])
                loc=location['name']
                temp.append(loc)
            else:
                pass

        instadetails['Location']=temp
        instadetails['ProfilePic'] = data2['profile_pic_url']

    except:
        instadetails['Error']="Profile not found"
    
    if "Name" in instadetails.keys() and instadetails['Name']!=None:
        return instadetails
    else:
        instadata={}
        cookies['rur']="ATN"
        r = tr.get("https://www.instagram.com/"+ username +"/?__a=1", headers=headers, cookies=cookies, verify=False)
        if r.status_code == 200:
            try:
                res = r.json()['graphql']['user']
            except:
                return {'Error':'Something Went Wrong'}
            instadata['Name']= res['full_name']
            instadata['URL']= str(res['external_url'])
            instadata['Bio']= res['biography']
            instadata['Followers'] = str(res['edge_followed_by']['count'])
            instadata['Following'] = str(res['edge_follow']['count'])
            instadata['No_of_posts'] = len(res['edge_owner_to_timeline_media']['edges'])
            instadata['Location']=list()
            for posts in res['edge_owner_to_timeline_media']['edges']:
                if posts['node']['location'] != None:
                    instadata['Location'].append(posts['node']['location']['name'])
                
            instadata['ProfilePic'] = res['profile_pic_url_hd']

        elif r.status_code == 404:
            instadata["Error"] = "Profile Not Found"
        else:
            instadata["Error"] = "Something Went Wrong"

        return instadata
'''

def Instagram(username):
    instadata={}
    r = requests.get("https://www.instagram.com/"+ username +"/?__a=1")
    if r.status_code == 200:
        res = r.json()['graphql']['user']
        
        instadata['username']=res['username']
        instadata['Name']=res['full_name']
        instadata["Biograph"]=res['biography']
        instadata["URL"]=str(res['external_url'])
        instadata["Followers"]=str(res['edge_followed_by']['count'])
        instadata["Following"]=str(res['edge_follow']['count'])
        instadata["Business"]=res['is_business_account']
        instadata["Joined_recently"]=res['is_joined_recently']
        instadata["private"]=res['is_private']
        instadata['verified']=res['is_verified']
        instadata['connected_fb_page']=res['connected_fb_page']
        
        if instadata['private']!=True:
            instadata['No_of_posts'] = len(res['edge_owner_to_timeline_media']['edges'])
            instadata['Location']=list()
            for posts in res['edge_owner_to_timeline_media']['edges']:
                if posts['node']['location'] != None:
                    instadata['Location'].append(posts['node']['location']['name'])
            
    elif r.status_code == 404:
        instadata["Error"] = "Profile Not Found"
    else:
        instadata["Error"] = "Something Went Wrong"

    return instadata

#print(Instagram('sri_shyam'))
