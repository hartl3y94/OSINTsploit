import requests
import json
import urllib.parse

def ghostproject(email):
  url = ("https://scylla.sh/search?q=email%3A{0}&num=100&from=200.json").format(email)
  print(url)
  headers = {'Accept': 'application/json'}
  response = requests.get(url,headers=headers)
  data = response.json()
  print(data)
  for i in data:
      try:
          print(f"Email:{i['fields']['email']}\nPassword:{i['fields']['password']}\nDomain:{i['fields']['domain']}\n--------------------------\n")
      except:
          print(i['fields'],"\n--------------------------")

ghostproject("adithyanhaxor@gmail.com")