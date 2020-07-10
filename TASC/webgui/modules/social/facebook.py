from requests_html import HTMLSession
from torrequest import TorRequest
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re
import random
import ray


@ray.remote
def Facebook(username):

    tr=TorRequest(password='pass')
    tr.reset_identity() #Reset Tor

    proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
    }

    session = HTMLSession()

    cookies = {
    'fr': '0w1VmDcmGCpgNCDFk.AWXzszEET8bsLO3gWdB1YfrETVo.BexpgX.9N.F8C.0.0.BfBJYh.AWUdpvRY',
    'sb': 'RMjIXjr4_fl6vAGirzPG6h3G',
    'datr': 'RMjIXgziEBR87a5w6WlAfDX-',
    'c_user': '100025059800297',
    'xs': '29%3A6syzEQfpAPphww%3A2%3A1590216794%3A13272%3A4196',
    'wd': '1366x610',
    '_fbp': 'fb.1.1594117891560.16058725',
    'act': '1594117923486%2F0',
    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'TE': 'Trailers',
    }

    url = 'https://en-gb.facebook.com/'+str(username)
    response = session.get(url,proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    main_div = soup.div.find(id="globalContainer")

    fbdetails={}

    def find_name():
        name = main_div.find(id="fb-timeline-cover-name")
        while name == None:
          tr=TorRequest(password='pass')
          tr.reset_identity() #Reset Tor
        name=str(name.get_text())
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
