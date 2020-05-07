import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def ACT(number):

    url="https://mynet.actcorp.in/widget/web/guest/cfrwspay?p_auth=TVZXU3oW&p_p_id=actroiwebsitepay_WAR_actcfroiwebsitepaymentportlet&p_p_lifecycle=1&p_p_state=maximized&p_p_mode=view&_actroiwebsitepay_WAR_actcfroiwebsitepaymentportlet_action=proceedRoiGetBillInfo&_actroiwebsitepay_WAR_actcfroiwebsitepaymentportlet_javax.portlet.action=proceedRoiGetBillInfo"

    headers = {
        '$Host': 'mynet.actcorp.in',
        '$User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        '$Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        '$Accept-Language': 'en-US,en;q=0.5',
        '$Accept-Encoding': 'gzip, deflate',
        'Referer':'https://mynet.actcorp.in/widget/web/guest/cfrwspay/-/actroiwebsitepay_WAR_actcfroiwebsitepaymentportlet',
        '$Content-Type': 'application/x-www-form-urlencoded',
        '$Connection': 'close',
        '$Upgrade-Insecure-Requests': '1',
    }

    params = {"wshydusername":str(number)}

    response = requests.post(url, headers=headers,params=params,verify=False)

    actresult={} # Main Output

    try:

        soup = BeautifulSoup(response.content, 'html.parser')
        table=soup.find('table',{"class":'table table-striped table-bordered text-left'})

        for tr in table.find_all('tr')[1:]:

            td=tr.find_all('td')
            actresult[td[0].text]=td[1].text

    except:

        actresult['Error']="Enter a Invalid Phone Number"

    return actresult

#print(ACT('7010951718'))