from .basedata import getBasedata
from .toinews import getNews


def Namedetails(name):
    details = {}
    firstname = name.split(" ")
    details.update(getBasedata(firstname))

    details.update(getNews(name))

    print(details)