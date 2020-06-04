
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re
import random

def Facebook(username):
    session = requests.session()
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
    session.headers={"User-Agent":user_agent_list[random.randint(0,len(user_agent_list)-1)]}
    session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
    #print(session.get("http://httpbin.org/ip").text)
    #print(session.get("https://httpbin.org/user-agent").text)
    
    fbdetails={} # Main Output

    search_string = "https://en-gb.facebook.com/" + username
    response = session.get(search_string)
    session.close()
    soup = BeautifulSoup(response.text, 'html.parser')
    main_div = soup.div.find(id="globalContainer")

    def find_name():
        name = main_div.find(id="fb-timeline-cover-name").get_text()
        name=str(name)
        fbdetails["Name"]=name

    #finding work details of the user
    def find_eduwork_details():

        education = soup.find(id="pagelet_eduwork")
        apple=education.find(attrs={"class":"_4qm1"})

        if (apple.get_text() != " "):
            temp={}
            for category in education.find_all(attrs={"class":"_4qm1"}):
                #print(category.find('span').get_text() ) #prints -> Work : | prints -> Education :
                name = str(category.find('span').get_text())
                temp[name]=""
                if name=="Professional Skills":
                    for company in category.find_all(attrs={"class":"_3pw9 _2pi4"}):
                        if (company.get_text() != " "):
                            name1=str(company.get_text())
                            temp[name]=temp[name]+"\n"+name1
                        else:
                            continue
                else:
                    for company in category.find_all(attrs={"class":"_6a _6b"}):
                        if (company.get_text() != " "):
                            #print(company.get_text()) # OWASP Coimbatore, Stuxnoid, TPH Infosec | Sri krishna, Kamarajar etc.
                            name1=company.get_text()
                            temp[name]=temp[name]+"\n"+name1
                        else:
                            continue
                temp[name]=temp[name].split("\n")
                fbdetails['Work_Education']=temp
        else:
            #print("No work details found")
            fbdetails["Work_Education"]="Details Not found"

    #finding home details of the user
    def find_home_details():
        if(soup.find(id="pagelet_hometown") !=" "):

                home = soup.find(id="pagelet_hometown")

                for category in home.find_all(attrs={"class":"_4qm1"}):

                    name=str(category.find('span').get_text())

                    for company in category.find_all(attrs={"class":"_42ef"}):
                        if (company.get_text() != " "):
                            homecom = company.get_text()
                            if "Home Town" in homecom:
                                homecom = homecom.replace("Home Town","")
                                fbdetails["Home_Town"]=str(homecom)
                            elif "Current city" in homecom:
                                homecom = homecom.replace("Current city", "")
                                fbdetails["Current_city"]=str(homecom)

                        else:
                            continue

        else:

            fbdetails["Home"]="Details Not found"

    #finding contact details of the user

    def find_contact_details():
        contact = soup.find(id="pagelet_contact")
        orange = contact.find(attrs={"class":"_4qm1"})
        if (orange.get_text() !=" "):
            for category in contact.find_all(attrs={"class":"_4qm1"}):
                name = str(category.find('span').get_text())
                for company in category.find_all(attrs={"class":"_2iem"}):
                    if (company.get_text() != " "):
                        name1 = str(company.get_text())
                    else:
                        continue
                fbdetails['Contact']=name1
        else:
             fbdetails['Contact']="Details Not Found"


    ###Logic for finding the status of the response

    if ("200" in str(response)):
        find_name()
        find_eduwork_details()
        find_home_details()
        find_contact_details()

        # ========================Facebook-ProfilePIC==========================

        try :

            pro = soup.find(attrs={"class": "_1nv3 _11kg _1nv5 profilePicThumb"})
            if pro:
                pass
            else:
                pro = soup.find(attrs={"class": "_1nv3 _11kg _1nv5"})
                pro= soup.find(attrs={"class":"_3016 _ttp profilePicThumb"})
            Profile_pic = str(pro.find(attrs={"class": "_11kf img"}))
            profiepiclink = re.findall(r'src="(.*?)"/>', Profile_pic)
            final = profiepiclink[0].replace("amp;", '')
            final = str(final)
            fbdetails["ProfilePic"]=final
            return fbdetails
        except:

            fbdetails['ProfilePic']="Details Not Found"
            return fbdetails

    elif ("404" in str(response)):

        fbdetails['Error']="Profile Not Found"
        return fbdetails


    else:
        
        fbdetails['Error']="Something Went Wrong"
        return fbdetails
    
#print(Facebook("akinfosec"))
