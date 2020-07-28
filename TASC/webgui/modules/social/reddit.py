import requests 
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def reddit(username):
    session = HTMLSession()
    session.get("https://reddit.com/")

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'TE': 'Trailers',
    }

    response = session.get('https://old.reddit.com/user/{}/'.format(username), headers=headers)
    soup = BeautifulSoup(response.text,"html.parser")

    
    try:
        reddit = {}
        #reddit["profile_img"]=soup.find("img",attrs={"class":"_2TN8dEgAQbSyKntWpSPYM7 _3Y33QReHCnUZm9ewFAsk8C"})['src']
        reddit['username']=soup.find("div",attrs={"class":"titlebox"}).find("h1").text

        '''try:
            reddit['name']=soup.find("h4",attrs={"class":"_3W1eUu5jHdcamkzFiJDITJ"}).text
        except AttributeError:
            pass

        try:
            reddit['bio']=soup.find("div",attrs={"class","bVfceI5F_twrnRcVO1328"})
        except:
            pass

        reddit['joined_on']=soup.find("span",attrs={"id":"profile--id-card--highlight-tooltip--cakeday"})

        try:
            response = session.get("https://old.reddit.com/user/unlimited/posts/",headers=headers)
            soup=BeautifulSoup(response.text,"html.parser")

            reddit['posts'] = [posts.text for posts in soup.find_all("h3")]
        except:
            pass'''

        response = session.get('https://old.reddit.com/user/unlimited/submitted/', headers=headers)
        soup = BeautifulSoup(response.text,"html.parser")
        reddit['posts']=[posts.text for posts in soup.find_all("a",attrs={"class":"title"})]
        return reddit
    except:
        return None