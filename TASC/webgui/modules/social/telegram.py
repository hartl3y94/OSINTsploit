import requests
from bs4 import BeautifulSoup

def telegram(username):
  response = requests.get("https://telegram.me/{}".format(username))

  soup = BeautifulSoup(response.content,"html.parser")
  data={}
  try:
    try:
      data['profileimg']=soup.find("img",attrs={"class":"tgme_page_photo_image"})['src']
    except:
      pass
    data['fullname']=soup.find("div",attrs={"class":"tgme_page_title"}).find("span").text.strip()
    data['username']=soup.find("div",attrs={"class":"tgme_page_extra"}).text.strip()

    return data
  except:
    return None