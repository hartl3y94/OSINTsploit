
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json,re


def Facebook(url):



    search_string = url
    response = requests.get(search_string)
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('li')
 

    for row in rows:

        for a in row.find_all('a', href=True): 
            if a.text: 
                print(a['href'])
      

Facebook("https://socialmedialist.org/social-media-apps-201-250.html")