
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import urllib.request
import json,re

def Facebook(username):

    #facebookdata = {}

    fburl = "https://en-gb.facebook.com/" + username
    response = requests.get(fburl)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_div = soup.div.find(id="globalContainer")

    #finding name of the user

    def find_name():

        fb_name = {}

        name = main_div.find(id="fb-timeline-cover-name").get_text()
        fb_name.update( {'Name' : name} )

    #finding profile pic of the user
    #link = main_div.find_all(name="img")

    ###Finding About the user details
    #finding work details of the user

    def find_eduwork_details():
        education = soup.find(id="pagelet_eduwork")
        educationdetails=education.find(attrs={"class":"_4qm1"})

        fb_work = {}

        if (educationdetails.get_text() != " "):
           
            for category in education.find_all(attrs={"class":"_4qm1"}):
                
                name = str(category.find('span').get_text())

                for company in category.find_all(attrs={"class":"_2tdc"}):
                    if (company.get_text() != " "):
        
                        company_name =str(company.get_text())

                        fb_work.update( {'Work & Education' : company_name} )

                    else:
                        continue
        else:
            
            fb_work.update( {'Work & Education' : 'Not Found'} )

    #finding home details of the user
    def find_home_details():

        fb_home = {}

        if(soup.find(id="pagelet_hometown") !=" "):
                home = soup.find(id="pagelet_hometown")
                for category in home.find_all(attrs={"class":"_4qm1"}):
        
                    name=str(category.find('span').get_text())

                    for company in category.find_all(attrs={"class":"_42ef"}):
                        if (company.get_text() != " "):
                            homecom = company.get_text()
                            homecom = homecom.replace("Home Town"," -> Home Town")
                            homecom = homecom.replace("Current city", " -> Current City")
                            fb_home.update( {name:homecom} )


                        else:

                            continue

        else:

            fb_home.update( {'Current City / Home Town' : 'Not Found'} )

    #finding contact details of the user
    def find_contact_details():

        fb_contact = {}

        contact = soup.find(id="pagelet_contact")
        orange = contact.find(attrs={"class":"_4qm1"})
        if (orange.get_text() !=" "):
            for category in contact.find_all(attrs={"class":"_4qm1"}):
                
                name = str(category.find('span').get_text())
             
                for company in category.find_all(attrs={"class":"_2iem"}):

                    if (company.get_text() != " "):
                        name1 = str(company.get_text())
                        fb_contact.update( {name : name1} )

                    else:
                        continue
        else:
             fb_contact.update( {'Contact Details' : 'Not Found'} )


    ###Logic for finding the status of the response

    if ("200" in str(response)):

        find_name()
        find_eduwork_details()
        find_home_details()
        find_contact_details()
        facebookdata = dict(fb_name, fb_work, fb_home, fb_contact)

        # ========================Facebook-ProfilePIC==========================

        try :
            pro = soup.find(attrs={"class": "_1nv3 _1nv5 profilePicThumb"})
            Profile_pic = str(pro.find(attrs={"class": "_11kf img"}))
            profiepiclink = re.findall(r'src="(.*?)"/>', Profile_pic)
            final = profiepiclink[0].replace("amp;", '')
            facebookdata.update( {'ProfilePicLink' : final} )
            print(facebookdata)
            return facebookdata

        except:
            facebookdata.update( {'ProfilePicLink' : 'Not Found'} )
            print(facebookdata)
            return facebookdata


    elif ("404" in str(response)):

        facebookdata.update( {'Profile' : 'Not Found'} )
        return facebookdata

    else:

        facebookdata.update( {'Profile' : 'Unknown Error'} )
        return facebookdata

Facebook('akinfosec')

#++++++++++++Twitter+++++++++++++#

def ScrapTweets(username):
    f = open("./output", "a")
    f.write("\n")
    print()
    f.write("Twitter Information : " + "\n")
    f.write("\n")
    username = username
    link = "https://twitter.com/" + username
    try :
        the_client = uReq(link)
        page_html = the_client.read()
        the_client.close()
    except:
        print("Profile Not Found")
        print()
        f.write("Profile not found")
        f.write("\n")
        return

    # print(link)

    soup = BeautifulSoup(page_html, 'html.parser')

    ######################################################################
    try:
        full_name = soup.find('a', attrs={"class": "ProfileHeaderCard-nameLink u-textInheritColor js-nav"})
        print()
        print("User Name : " + full_name.text)
        twittername = str(full_name.text)
        f.write("User Name : " + twittername + "\n")
    except:
        print("User Name : Not Found")
    print()

    try:
        user_id = soup.find('b', attrs={"class": "u-linkComplex-target"})
        print("User Id : " + user_id.text)
        twitterid = str(user_id.text)
        f.write("User ID : " + twitterid + "\n")
    except:
        print("User Id : Not Found")
    print()

    try:
        decription = soup.find('p', attrs={"class": "ProfileHeaderCard-bio u-dir"})
        print("Description : " + decription.text)
        twitterdesc = str(decription.text)
        f.write("Description : " + twitterdesc + "\n")
    except:
        print("Description : Not provided by the user")
    print()

    try:
        user_location = soup.find('span', attrs={"class": "ProfileHeaderCard-locationText u-dir"})
        print("Location : " + user_location.text.strip())
        twitterloc = str(user_location.text.strip())
        f.write("Location : " + twitterloc + "\n")
    except:
        print("Location : Not provided by the user")
    print()

    try:
        connectivity = soup.find('span', attrs={"class": "ProfileHeaderCard-urlText u-dir"})
        tittle = connectivity.a["title"]
        print("Web Link : " + tittle)
        twitterlink = str(tittle)
        f.write("Web Link : " + twitterlink + "\n")

    except:
        print("No contact link is provided by the user")
    print()

    try:
        join_date = soup.find('span', attrs={"class": "ProfileHeaderCard-joinDateText js-tooltip u-dir"})
        print("Twitter Join Date : " + join_date.text)
        twitterjoin = str(join_date.text)
        f.write("Twitter Join Date : " + twitterjoin + "\n")
    except:
        print("The joined date is not provided by the user")
    print()

    try:
        birth = soup.find('span', attrs={"class": "ProfileHeaderCard-birthdateText u-dir"})
        birth_date = birth.span.text
        bday = birth_date.strip()
        bday = bday.replace("Born",'')
        print("Birthday :"+bday)
        twitterbday = str(bday)
        f.write("Birthday : " + twitterbday + "\n")

    except:
        print("Birth Date not provided by the user")
    print()

    ###########################################################################
    try:
        span_box = soup.findAll('span', attrs={"class": "ProfileNav-value"})
        print("Total Tweets : " + span_box[0].text)
        twittertotaltweets = str(span_box[0].text)
        f.write("Total Tweets : " + twittertotaltweets + "\n")
        print()
    except:
        print("Total Tweets : Zero")
        print()

    try:
        print("Following : " + span_box[1].text)
        twitterfollowing = str(span_box[1].text)
        f.write("Following : " + twitterfollowing + "\n")
    except:
        print("Following : Zero")
    print()

    try:
        print("Followers : " + span_box[2].text)
        tfollowers = str(span_box[2].text)
        f.write("Followers : " + tfollowers + "\n")
    except:
        print("Followers : Zero")
    print()

    try:
        print("Tweets liked : " + span_box[3].text)
        tliked = str(span_box[3].text)
        f.write("Tweets liked : " + tliked + "\n")
    except:
        print("Tweets liked : Zero")
    print()

    try:
        if span_box[4].text != "More ":
            print("Subscribed to : " + span_box[4].text)
            tsubs = str(span_box[4].text)
            f.write("Subscribed to : " + tsubs + "\n")
        else:
            print("Subscribed to : Zero")
    except:
        print("Subscribed to : Zero")
    print()

    spana = soup.findAll('span', attrs={"class": "ProfileNav-value"})

    ###########################################################################
    print("Tweets by " + username + " : ")
    f.write("Tweets by : " + username + " : "+ "\n")
    print()
    # TweetTextSize TweetTextSize--normal js-tweet-text tweet-text
    for tweets in soup.findAll('p', attrs={"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}):

        print(tweets.text)
        ttweet = tweets.text
        f.write(ttweet + "\n")
        print()


    print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->")
    print()
    return


#==========================INSTAGRAM=============================


def Instgram(username):

    try:

        f = open("./output", "a")
        f.write("\n")

        f.write("Instragram Information : " + "\n")
        f.write("\n")

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



        print()
        response = requests.get('https://www.instagram.com/'+user_name, headers=headers, verify=False)
        soup = BeautifulSoup(response.content, features="lxml")
        l=soup.findAll('script',type='text/javascript')[3].text
        l=l[l.find("=")+2:len(l)-1:]
        data=json.loads(l)
        data1=data['entry_data']['ProfilePage']
        data2=data1[0]['graphql']['user']
        url=data2['external_url']
        Name=data2['full_name']
        print("Name: ",Name)
        f.write("Name : " + Name + "\n")

    #+++++++++++++++++++Instgram_DP++++++++++++++++++++#



        if url is not None:
            print("URL: ",url)
            f.write("URL : " + url + "\n")
        print("Bio: ",data2['biography'])
        bio = data2['biography']
        f.write("Bio : " + bio + "\n")
        print("Followers: ",data2['edge_followed_by']['count'])
        followers = str(data2['edge_followed_by']['count'])
        f.write("Followers : " + followers + "\n")
        print("Following: ",data2['edge_follow']['count'])
        following = str(data2['edge_follow']['count'])
        f.write("Following : " + following + "\n")
        print("No.of.posts: ",data2['edge_owner_to_timeline_media']['count'])
        no_posts = str(data2['edge_owner_to_timeline_media']['count'])
        f.write("No.of.posts : " + no_posts + "\n")
        data3=data2['edge_owner_to_timeline_media']['edges']
        img_contents=[]
        locations=[]
        captions=[]
        for i in range(0,len(data3)):


            #print("Image contents: ",content)
            location=data3[i]['node']['location']
            if location is not None:
                #print("Location: ",location['name'])
                locations.append(location['name'])
            else:
                pass
            cap1=data3[i]['node']['edge_media_to_caption']
            cap2=cap1['edges']
            if cap2 is not None:
                try:
                    cap3=cap2[0]['node']['text']
                    captions.append(cap3)
                except:
                    pass
                #print("caption: ",cap3)
            else:
                pass
        #if len(locations)>0:
         #   print("Locations: ",locations)
        print()
        print("Locations : ")
        f.write("\n")
        f.write("Locations : " + "\n")
        f.write("\n")
        print()
        for z in locations:
            print(z)
            f.write(z + "\n")

        dp_url = data2['profile_pic_url']
        urllib.request.urlretrieve(dp_url, "dp.jpg")
        image_window = tk.Tk()
        img = ImageTk.PhotoImage(Image.open('dp.jpg'))
        panel = tk.Label(image_window, image=img)
        panel.pack(side="bottom", fill="both", expand="yes")
        image_window.mainloop()


    except:

        print("Profile not found")
        f.write("Profile not found")
        return

    print()
    print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->")
    print()
    return
