from .basedata import getBasedata
from .toinews import getNews


def Namedetails(name):
    details = {}
    #firstname = str(name.split(" ")[0])
    details['basedata']=getBasedata(name)
    details['news']=getNews(name)

    return details