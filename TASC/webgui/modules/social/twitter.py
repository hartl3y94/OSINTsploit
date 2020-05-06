
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re

def Twitter(username):

    twitterdetails={}

    username = username

    link = "https://twitter.com/" + username

    try :
        the_client = uReq(link)
        page_html = the_client.read()
        the_client.close()

    except:

        twitterdetails['Error']="Profile Not Found"
        return

    soup = BeautifulSoup(page_html, 'html.parser')

    try:

        full_name = soup.find('a', attrs={"class": "ProfileHeaderCard-nameLink u-textInheritColor js-nav"})
        twitterdetails["User Name"]=str(full_name.text)

    except:

        twitterdetails["User Name"]="Not Found"

    try:

        user_id = soup.find('b', attrs={"class": "u-linkComplex-target"})
        twitterdetails["User Id"]=str(user_id.text)

    except:
        twitterdetails["User Id"]="Not Found"

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
        twitterdetails["Web Link"]=str(tittle)

    except:
        twitterdetails["Web Link"]="No contact link is provided by the user"

    try:
        join_date = soup.find('span', attrs={"class": "ProfileHeaderCard-joinDateText js-tooltip u-dir"})
        twitterdetails["Twitter Join Date"]=str(join_date.text)

    except:
        twitterdetails["Twitter Join Date"]="The joined date is not provided by the user"

    try:
        birth = soup.find('span', attrs={"class": "ProfileHeaderCard-birthdateText u-dir"})
        birth_date = birth.span.text
        bday = birth_date.strip()
        bday = bday.replace("Born",'')
        twitterdetails["Birthday :"]=str(bday)

    except:
        twitterdetails["Birthday :"]="Birth Date not provided by the user"

    ###########################################################################
    try:
        span_box = soup.findAll('span', attrs={"class": "ProfileNav-value"})
        twitterdetails["Total Tweets"]=str(span_box[0].text).strip()
    except:
        twitterdetails["Total Tweets"]="Zero"

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


print(Twitter('adithyan_ak'))