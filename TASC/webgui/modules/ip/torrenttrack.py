import cfscrape
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

def GetTorrent(ipaddr):

    ip = str(ipaddr)
    url = 'https://iknowwhatyoudownload.com/en/peer/?ip=' + ip
    scraper = cfscrape.create_scraper()
    response = scraper.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    downloads = soup.find(attrs={"class": "table table-condensed table-striped"})
    final = downloads.find_all(attrs={"class": "name-column"})
    size = downloads.find_all(attrs={"class": "size-column"})
    date = downloads.find_all(attrs={"class": "date-column"})
    categ = downloads.find_all(attrs={"class": "category-column"})

    Downloads = {}

    if final == []:

        return Downloads

    else:

        i = 0

        for z in final:

            Downloads.update({i + 1: {'Title': '', 'Category': '', "Size": '', 'Date': ''}})

            name = z.get_text()
            siz = size[i].get_text()
            dates = date[i].get_text()
            category = categ[i].get_text()
            file_name = name.strip()

            Downloads[i+1]['Title'] = file_name

            Downloads[i+1]['Category'] = category

            Downloads[i+1]['Size'] = siz

            Downloads[i+1]['Date'] = dates

            i = i + 1

        return Downloads




