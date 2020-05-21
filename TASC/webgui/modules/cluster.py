
from .social.facebook import Facebook
from .social.instagram import Instagram
from .social.twitter import Twitter
from .social.fbkeyword import FacebookScrapper
from .social.locmap import loc,heat_map, gps_map
from .ip.ipstack import IPtrace
from .ip.torrenttrack import GetTorrent
from .ip.multipleip import read_multiple_ip
from .ip.maclookup import macLookup
from .ip.portscan import DefaultPort
from .ip.censys import censys_ip
from .ip.shodan import shodan_ip
from .phone.phonenum import HLRlookup
from .email.hibp import HaveIbeenPwned
from .email.hunter import hunter
from .email.emailrep import emailrep
from .domain.webosint import getDomain
from django.contrib.auth.models import User
from .btc.btc import btcaddress
import os

def MakeCluster(request):
    username = request.user.username
    user = User.objects.filter(username=username).first()
    url = user.profile.clusterjson.url
    return url

