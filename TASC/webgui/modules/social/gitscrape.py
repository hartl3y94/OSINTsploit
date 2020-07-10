import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import random
import ray

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

headers={
  'User-Agent':user_agent_list[random.randint(0,len(user_agent_list)-1)],
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

session.headers=headers
session.proxies = {'http':  'socks5://127.0.0.1:9050','https': 'socks5://127.0.0.1:9050'}

def getrepos(username):
  r = session.get("https://api.github.com/users/"+username+"/repos?page=2&per_page=5",headers=headers,verify=False)
  repos = []
  response = json.loads(r.content)
  if "message" in response and response["message"] == "Not Found":
    return []
  else:
    for repo in response:
      repos.append(repo['full_name'].split("/")[-1])
  return repos
  
def getgmails(repo,username):
  r = session.get("https://api.github.com/repos/"+username+"/"+repo+"/commits",headers=headers,verify=False)
  response = json.loads(r.content)
  emails = []
  if isinstance(response, list):
    for commit in response:
      got_email = commit['commit']['committer']['email']
      if not got_email == "noreply@github.com":
        emails.append(commit['commit']['committer']['email'])
  if len(emails)>0:
    return set(emails)

def getcommits(repo,username):
  commits=list()
  response=session.get("https://api.github.com/repos/"+username+"/"+repo+"/commits",headers=headers,verify=False)
  data=json.loads(response.content)
  for i in range(len(data)):
    commits.append({"Head":data[i]["sha"],"Message":data[i]["commit"]["message"],"Author":data[i]["author"]["login"]})
  if len(commits)>5:
    return commits[-5:]
  else:
    return commits
    
def getprofile(username):
  response=session.get("https://api.github.com/users/"+username,headers=headers,verify=False)
  if response.status_code==200:
    return json.loads(response.content)
  else:
    return None

@ray.remote
def gitscrape(username):
  gitdata={}
  #print(session.get("http://httpbin.org/ip").text)
  #print(session.get("https://httpbin.org/user-agent").text)

  profile=getprofile(username)
  if profile!=None:
    gitdata['Profile']=profile

    repos=getrepos(username)
    gitdata['Repository']=repos

    mail = []
    for repo in repos:
      mails=getgmails(repo, username)
      if mails!=None:
        for i in mails:
          mail.append(i)
    gitdata['Mails']=list(set(mail))

    return gitdata
  else:
    return None

session.close()
