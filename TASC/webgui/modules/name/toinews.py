import requests
from bs4 import BeautifulSoup
result=[]
def getNews(key):
    page = 2
    for i in range(1,page+1):
        key = key+" cyber crime"
        key=key.replace(" ","+")
        url="https://timesofindia.indiatimes.com/searchresult.cms?sortorder=score_artdate&searchtype=2&maxrow=10&startdate=2001-01-01&enddate=2001-08-01&article=2&pagenumber={}&isphrase=no&query={}&searchfield=&section=&kdaterange=1500&date1mm=01&date1dd=01&date1yyyy=2001&date2mm=08&date2dd=01&date2yyyy=2001".format(i,key)
        response = requests.post(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        temp=soup.find_all(class_='maintable12')
        soup = BeautifulSoup(str(temp), 'html.parser')
        div_tag=soup.find_all('div')
        for x in div_tag:
            soup = BeautifulSoup(str(x), 'html.parser')
            aa=soup.find('a')
            if soup.find('span') != None and aa!=None:
                if aa.text not in('Next »','«Previous','Advanced Search','Date','Relevance'):
                    info = {
                    "title":  aa.text,
                    "link":"www.timesofindia.com/"+str(aa['href']),
                    "date":str(soup.find('span').text)[4:21]
                    }
                    result.append(info)
    return result

print(getNews("Manoj Abraham"))