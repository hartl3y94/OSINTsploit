import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def emailrep(email,apikey):
    return {'email': 'aravindha1234u@gmail.com', 'reputation': 'high', 'suspicious': False, 'references': 10, 'details': {'blacklisted': False, 'malicious_activity': False, 'malicious_activity_recent': False, 'credentials_leaked': True, 'credentials_leaked_recent': False, 'data_breach': True, 'first_seen': '09/10/2014', 'last_seen': '05/24/2019', 'domain_exists': True, 'domain_reputation': 'n/a', 'new_domain': False, 'days_since_domain_creation': 9040, 'suspicious_tld': False, 'spam': False, 'free_provider': True, 'disposable': False, 'deliverable': True, 'accept_all': False, 'valid_mx': True, 'spoofable': True, 'spf_strict': True, 'dmarc_enforced': False, 'profiles': ['spotify', 'pinterest', 'twitter', 'gravatar']}}
    headers = {
        'Key':apikey,
        'User-Agent':'TASC',
        }
    url="https://emailrep.io/"+email
    response=requests.get(url,headers=headers,verify=False)
    data=response.text
    return json.loads(data)