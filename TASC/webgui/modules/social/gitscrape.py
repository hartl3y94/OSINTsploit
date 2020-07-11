import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import random

session = requests.session()

def getrepos(username):
  r = session.get("https://api.github.com/users/"+username+"/repos?page=2&per_page=5",verify=False)
  repos = []
  response = json.loads(r.content)
  if "message" in response and response["message"] == "Not Found":
    return []
  else:
    for repo in response:
      repos.append(repo['full_name'].split("/")[-1])
  return repos
  
def getgmails(repo,username):
  r = session.get("https://api.github.com/repos/"+username+"/"+repo+"/commits",verify=False)
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
  response=session.get("https://api.github.com/repos/"+username+"/"+repo+"/commits",verify=False)
  data=json.loads(response.content)
  for i in range(len(data)):
    commits.append({"Head":data[i]["sha"],"Message":data[i]["commit"]["message"],"Author":data[i]["author"]["login"]})
  if len(commits)>5:
    return commits[-5:]
  else:
    return commits
    
def getprofile(username):
  response=session.get("https://api.github.com/users/"+username,verify=False)
  if response.status_code==200:
    return json.loads(response.content)
  else:
    return None

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
