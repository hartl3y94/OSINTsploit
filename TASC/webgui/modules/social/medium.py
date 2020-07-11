import requests
from bs4 import BeautifulSoup
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def medium(username):
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

    headers = {
        'User-Agent': user_agent_list[random.randint(0,len(user_agent_list)-1)],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'Trailers',
    }

    session.headers=headers
    session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}
    #print(session.get("http://httpbin.org/ip").text)
    #print(session.get("https://httpbin.org/user-agent").text)
    
    url="https://medium.com/@"+username
    try:
        response = session.get(url,verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,"html.parser")
            try:
                full_name = soup.find('h1',{'class' :  'av q dp cj dq ck dr ds dt y'})
                is_paid_member = True
                bio = soup.find('p',{'class' : 'eq er cj b ck es et cn y'})
                subtitle = soup.find_all('a',{'class' :'cd ce bm bn bo bp bq br bs bt ex bw bx ch ci'})
                img=soup.findAll("img")[0].get('src')
                try:
                    extra_info = [subtitle[i].text for i in range(5) if len(subtitle) > 0]
                except:
                    extra_info=None
                return {'full_name' : full_name.text,'is_paid_member' : is_paid_member,'bio' : bio.text,'extras' : extra_info,'Profile_pic':img}
            except:
                full_name = soup.find('h1',{'class' : 'av q dh cj di ck dj dk dl y'})      
                is_paid_member = False
                bio = soup.find('p',{'class' : 'ei ej cj b ck ek el cn y'})
                subtitle = soup.find_all('a',{'class' : 'cd ce bm bn bo bp bq br bs bt eo bw bx ch ci'})
                img=soup.findAll("img")[0].get('src')
                try:
                    extra_info = [subtitle[i].text for i in range(5) if len(subtitle) > 0]
                except:
                    extra_info=None
                return {'full_name' : full_name.text,'is_paid_member' : is_paid_member,'bio' : bio.text,'extras' : extra_info,'Profile_pic':img}
    except:
        return None