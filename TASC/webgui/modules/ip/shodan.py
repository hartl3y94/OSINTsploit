import shodan
from core.config import shodan_api

api = shodan.Shodan(shodan_api)


def shodan_host(IP):
    try:
        host = api.host(IP)
        print("\n[+] Gathering IP Address Information from [shodan]\n")
        print("IP Address ----> " + str(host['ip_str']))
        print("Country -------> " + str(host['country_name']))
        print("City ----------> " + str(host['city']))
        print("Organization --> " + str(host['org']))
        print("ISP -----------> " + str(host['isp']))
        print("Open ports ----> " + str(host['ports']))
    except:
        print("Unavailable")


def shodan_ip(IP):
    try:
        host = api.host(IP)
        print("\n[+] Gathering Domain Information from [shodan]\n")
        print("IP Address ----> " + str(host['ip_str']))
        print("Country -------> " + str(host['country_name']))
        print("City ----------> " + str(host['city']))
        print("Organization --> " + str(host['org']))
        print("ISP -----------> " + str(host['isp']))
        print("Open ports ----> " + str(host['ports']))
    except:
        print("Unavailable")

def honeypot(inp):
    honey = 'https://api.shodan.io/labs/honeyscore/%s?key=%s' % (inp, shodan_api)
    try:
        result = get(honey).text
    except:
        result = None
        sys.stdout.write('\n%s No information available' % bad + '\n')
    if "error" in result or "404" in result:
        print("IP Not found")
        return
    elif result:
            probability = str(float(result) * 10)
            print('\n[+] Honeypot Probabilty: %s%%' % (probability) + '\n')
    else:
        print("Something went Wrong")
