import random
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re
from requests_html import HTMLSession, HTML
import ray

@ray.remote
def Twitter(username):

    session = HTMLSession()
    user_agent_list = [
    #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]
    session.headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Referer": "https://twitter.com/{}".format(username),
            "User-Agent": user_agent_list[random.randint(0,len(user_agent_list)-1)],
            "X-Twitter-Active-User": "yes",
            "X-Requested-With": "XMLHttpRequest",
            "Accept-Language": "en-US",
        }
    #session.headers={"User-Agent":user_agent_list[random.randint(0,len(user_agent_list)-1)]}
    session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
    #print(session.get("http://httpbin.org/ip").text)
    #print(session.get("https://httpbin.org/user-agent").text)

    twitterdetails={}

    username = username

    link = "https://twitter.com/" + username
    try :
        '''the_client = uReq(link)
        page_html = the_client.read()
        the_client.close()'''
        page_html=session.get(link,verify=False).content
    except:
        twitterdetails['Error']="Profile Not Found"
        return twitterdetails
    #print(page_html)
    soup = BeautifulSoup(page_html, 'html.parser')
    
    session.close()
    try:

        profile_pic_url= str(soup.findAll('img')[4]).split("src=\"")[1][:-3]
        twitterdetails["ProfilePic"]=profile_pic_url
    except:
        twitterdetails["ProfilePic"]=""

    try:

        full_name = soup.find('a', attrs={"class": "ProfileHeaderCard-nameLink u-textInheritColor js-nav"})
        twitterdetails["User_Name"]=str(full_name.text)

    except:

        twitterdetails["User_Name"]="Not Found"

    try:

        user_id = soup.find('b', attrs={"class": "u-linkComplex-target"})
        twitterdetails["User_Id"]=str(user_id.text)

    except:
        twitterdetails['Error']="Profile Not Found"
        return twitterdetails

    try:
        decription = soup.find('p', attrs={"class": "ProfileHeaderCard-bio u-dir"})
        twitterdetails["Description"]=str(decription.text)

    except:
        twitterdetails["Description"]="Not provided by the user"

    try:
        user_location = soup.find('span', attrs={"class": "ProfileHeaderCard-locationText u-dir"})
        twitterdetails["Location"]=str(user_location.text.strip())

    except:
        twitterdetails["Location"]="Not provided by the user"

    try:
        connectivity = soup.find('span', attrs={"class": "ProfileHeaderCard-urlText u-dir"})
        tittle = connectivity.a["title"]
        twitterdetails["Web_Link"]=str(tittle)

    except:
        twitterdetails["Web_Link"]="No contact link is provided by the user"

    try:
        join_date = soup.find('span', attrs={"class": "ProfileHeaderCard-joinDateText js-tooltip u-dir"})
        twitterdetails["Twitter_Join_Date"]=str(join_date.text)

    except:
        twitterdetails["Twitter_Join_Date"]="The joined date is not provided by the user"

    try:
        birth = soup.find('span', attrs={"class": "ProfileHeaderCard-birthdateText u-dir"})
        birth_date = birth.span.text
        bday = birth_date.strip()
        bday = bday.replace("Born",'')
        twitterdetails["Birthday"]=str(bday)

    except:
        twitterdetails["Birthday"]="Birth Date not provided by the user"

    ###########################################################################
    try:
        span_box = soup.findAll('span', attrs={"class": "ProfileNav-value"})
        twitterdetails["Total_Tweets"]=str(span_box[0].text).strip()
    except:
        twitterdetails["Total_Tweets"]="Zero"

    try:
        twitterdetails["Following"]=str(span_box[1].text)
    except:
        twitterdetails["Following"]="Zero"

    try:
        twitterdetails["Followers"]=span_box[2].text
    except:
        twitterdetails["Followers"]="Zero"

    try:
        twitterdetails["Followers"]= str(span_box[3].text)
    except:
        twitterdetails["Followers"]="Zero"

    try:
        if span_box[4].text != "More ":
            twitterdetails["Followers"]=str(span_box[4].text)
        else:
            twitterdetails["Followers"]="Zero"
    except:
        twitterdetails["Followers"]="Zero"

    ###########################################################################

    twitterdetails['Tweets']={}

    i=0

    for tweets in soup.findAll('p', attrs={"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):

        if i < 10: # Remove the limit to load all the first page tweets

            twitterdetails['Tweets'][str(i)]=tweets.text
            i+=1

        else:
            pass

    return twitterdetails

#print(Twitter("bhavsec"))
