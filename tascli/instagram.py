import requests
import json
{'Name': 'Adithyan Ak', 'URL': 'https://www.google.com/search?q=adithyan+ak', 'Bio': 'Breaking and Building Code', 'Followers': 223, 'Following': 42, 'No_of_posts': 11, 'Location': ['Cyber Hub Gurgaon', 'Commissioner of Police Gurgaon', 'LMR Theatre Namakkal', 'Kuniyamuthur'], 'ProfilePic': 'https://instagram.fcjb1-1.fna.fbcdn.net/v/t51.2885-19/s150x150/95732872_1253059848419907_1481650351458222080_n.jpg?_nc_ht=instagram.fcjb1-1.fna.fbcdn.net&_nc_ohc=Qc0GE0oNbtkAX-Szajy&oh=8d076b0ff657a83f7d0255c34f118190&oe=5F2DB49B'}


def Instagram(username):
    instadata={}
    r = requests.get("https://www.instagram.com/"+ username +"/?__a=1")
    if r.status_code == 200:
    	
        res = r.json()['graphql']['user']
        instadata['Name']= res['full_name']
        instadata['URL']= str(res['external_url'])
        instadata['Bio']= res['biography']
        instadata['Followers'] = str(res['edge_followed_by']['count'])
        instadata['Following'] = str(res['edge_follow']['count'])
        instadata['No_of_posts'] = len(res['edge_owner_to_timeline_media']['edges'])
        instadata['Location']=list()
        for posts in res['edge_owner_to_timeline_media']['edges']:
            if posts['node']['location'] != None:
                instadata['Location'].append(posts['node']['location']['name'])
            
        instadata['ProfilePic'] = res['profile_pic_url_hd']

    elif r.status_code == 404:
        instadata["Error"] = "Profile Not Found"
    else:
        instadata["Error"] = "Something Went Wrong"

    return instadata

print(Instagram("adithyan.ak"))
