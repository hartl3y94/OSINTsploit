
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time

def Instagram(username):
    instadetails={}
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    try:

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

        user_name=username
        #response = requests.get('https://www.instagram.com/'+user_name, headers=headers, verify=False)
        driver.get('https://www.instagram.com/'+user_name)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, features="lxml")
        l=soup.findAll('script',type='text/javascript')[3].text
        l=l[l.find("=")+2:len(l)-1:]
        data=json.loads(l)
        data1=data['entry_data']['ProfilePage']
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
            '''cap1=data3[i]['node']['edge_media_to_caption']
            cap2=cap1['edges']
            if cap2 is not None:
                try:
                    cap3=cap2[0]['node']['text']
                    temp[str(i)]["content"]=cap3
                except:
                    pass
            else:
                pass'''
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
    
    if 'Name' in instadetails.keys() and instadetails['Name']!=None:
        driver.close()
        driver.quit()
        return instadetails
    else:
        instadata={}
        try:
            r = requests.get("https://www.instagram.com/"+ username +"/?__a=1")
            res=r.json()['graphql']['user']
            if r.status_code == 200:
                pass
            elif r.status_code == 404:
                instadata["Error"] = "Profile Not Found"
            else:
                instadata["Error"] = "Something Went Wrong"
            
        except:
            driver.get("view-source:https://www.instagram.com/"+ username +"/?__a=1")
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source,"lxml")
            res=json.loads(soup.find("pre").contents[0])
            res = res['graphql']['user']
        
        if res != {}:
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
        else:
            instadata["Error"] = "Profile Not Found"
        
        driver.close()
        driver.quit()
        return instadata
    

#print(Instagram('adithyan.ak'))
