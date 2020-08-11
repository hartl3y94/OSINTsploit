import requests
import json

'''import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

def ghostproject(email):
  options = Options()
  options.headless = True
  driver = webdriver.Firefox(options=options)
  try:
    driver.get("https://ghostproject.fr/")
    time.sleep(8)
    try:
      #myElem = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'searchStr')))
      #myElem = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'btn')))
      myElem = WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.ID, 'banner')))
    except TimeoutException:
      time.sleep(5)
    driver.find_element_by_id("searchStr").send_keys(email)
    time.sleep(2)
    try:
      element = driver.find_element_by_class_name("btn")
      element.click()
    except selenium.common.exceptions.InvalidSelectorException:
      element = driver.find_element_by_xpath("/html/body/center/div/span/div/div/div/div[2]/div/div/div/div/div/div/div/div[5]/center/button")
      element.click()
    except selenium.common.exceptions.ElementClickInterceptedException:
      driver.execute_script("arguments[0].click();", element)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source,"html.parser")
    table=soup.find("table",attrs={'id':'result'})
    table_body = table.find('tbody')
    #print(table_body)
    data=list()
    rows = table_body.find_all('tr')
    for row in rows:
      cols = row.find_all('td')
      if "Error" in cols:
        driver.close()
        driver.quit()
        return None
      else:
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
    data=data[1:-1]
    data=[x[0] for x in data]
    driver.close()
    driver.quit()
    return ({x.split(":")[1]:len(x.split(":")[1]) for x in data})
  except:
    driver.close()
    driver.quit()
    return None
  
'''

def ghostproject(email):
  url = "https://scylla.sh/search?q=email%3A{}&num=100&from=200.json".format(email)
  response = requests.get(url,headers={'Accept': 'application/json'})
  data=[]
  if len(response.json())==0:
    return None
  for i in response.json():
    temp={}
    temp['email']=i['fields']['email']
    temp['password']=i['fields']['password']
    temp['domain']=i['fields']['domain']
    data.append(temp)
  
  return data

#print(ghostproject("adithyanhaxor@gmail.com"))