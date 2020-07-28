from bs4 import BeautifulSoup
import requests
import selenium
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

def linkedin(username):
	options = Options()
	options.headless = True

	driver = webdriver.Firefox(options=options)
	driver.get("https://www.linkedin.com/login")

	cookies = {
			'JSESSIONID': 'ajax:4690416897369399069',
			'bcookie': 'v=2&80bb5169-ad49-40f1-8d1d-4943d8632949',
			'bscookie': 'v=1&20200726060908bf79b390-f9ec-4883-8c13-394c6b9fbc52AQFHLRu-BJ-6h-pkdcPXFFzqSQDSNj2H',
			'lissc': '1',
			'lidc': 'b=OGST07:s=O:r=O:g=1754:u=1:i=1595743774:t=1595826056:v=1:sig=AQEeTTF9BS1Q0IIqkzp3dHxtlfM7iATA',
			'_ga': 'GA1.2.1713635130.1595743749',
			'_gat': '1',
			'AMCV_14215E3D5995C57C0A495C55%40AdobeOrg': '-408604571%7CMCIDTS%7C18470%7CMCMID%7C40690365609328188036766116916306264775%7CMCOPTOUT-1595750973s%7CNONE%7CvVersion%7C4.6.0',
			'AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg': '1',
			'li_at': 'AQEDATG5V8QAMdKsAAABc4m9cxYAAAFzrcn3FlYAOoYrL2gJua0fXyVOUT32PLe87Nh6vdiCjsu2wozq4lyVbNQTE2C9C5BbkR1RyfVBWEEaKI5ltKhVkVJuz0EiPi30I-30lt1FPoyLEqpwCxuDwcy2',
			'liap': 'true',
			'lang': 'v=2&lang=en-us',
			'UserMatchHistory': 'AQKyUs_5rkELkAAAAXOJvYdhAxmOs1i77_H3Ig1cW6k5UI5olgnqh9EJ7_VtKM53kfePdOr-wNCLKWtJERz2bjAG3obwmAOWdUdfTizqJcI1K37asmDy84IQblqKiloSWCGjHK1DKhGqrW9ksEoClOXXPxnE7g2tyHHvVeHDL5gPvJov_E3L9kSCaqOk7CEVeP-1EvDf0xlHQwH9pBZHnUcdLFawwEsqsY8hlWdnn9jd',
			'li_sugr': '188291f1-9f1c-4af1-8d36-e65e8c090ebe',
			'_guid': '4cf7efc0-9507-4580-a9d5-5a150889bd67',
			'li_oatml': 'AQEVPvQ5Hnw2xgAAAXOJvZn_Ma6WdlnVkHKyvRkxknxPdZIYFKnh6RLub3n92vI2lkDIlzwwofO0_JCsij9lemCcYE_cKUVT',
	}

	for keys,values in cookies.items():
		driver.add_cookie({"name":keys,"value":values})
	time.sleep(2)
	url ="https://www.linkedin.com/in/{}/".format(username)
	driver.get(url)
	driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
	time.sleep(1)
	if driver.current_url != url:
		return None
	source=driver.page_source

	soup = BeautifulSoup(source,"html.parser")

	linkedin={}
	
	linkedin['Profileimg']=soup.find("img",attrs={"class":"pv-top-card__photo presence-entity__image EntityPhoto-circle-9 lazy-image ember-view"})['src']
	linkedin['Name']=soup.find("li",attrs={"class":"inline t-24 t-black t-normal break-words"}).text.strip()
	linkedin['Bio']=soup.find("h2",attrs={"class":"mt1 t-18 t-black t-normal break-words"}).text.strip().replace("\n","")
	linkedin['Location']=soup.find("li",attrs={"class":"t-16 t-black t-normal inline-block"}).text.strip()
	linkedin['About']=soup.find("p",attrs={"class","pv-about__summary-text mt4 t-14 ember-view"}).text.strip()

	linkedin['Experience']=[]
	# get experience
	try:
		_ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "experience-section")))
		exp = driver.find_element_by_id("experience-section")
	except:
		exp = None

	if (exp is not None):
		for position in exp.find_elements_by_class_name("pv-position-entity"):
			position_title = position.find_element_by_tag_name("h3").text.strip()
			try:
					company = position.find_elements_by_tag_name("p")[1].text.strip()
			except:
					company = None
			linkedin['Experience'].append({"Position":position_title,"Company":company})

	# get education
	try:
		_ = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "education-section")))
		edu = driver.find_element_by_id("education-section")
	except:
		edu = None
	driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

	linkedin['Education']=[]
	if (edu is not None):
		for school in edu.find_elements_by_class_name("pv-profile-section__list-item"):
			university = school.find_element_by_class_name("pv-entity__school-name").text.strip()
			try:
					degree = school.find_element_by_class_name("pv-entity__degree-name").find_elements_by_tag_name("span")[1].text.strip()
			except:
					degree = None
			linkedin['Education'].append({"University":university,"Degree":degree})

	driver.quit()
	return linkedin