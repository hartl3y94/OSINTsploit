from .phonenum import HLRlookup, numverify
from .getcontact import getcontact
from .truecaller import TrueCaller

def Phone(request_data, apilayerphone, hlruname, hlrpwd):

    phone = {}

    if apilayerphone == "" or hlruname == "" or hlrpwd == "":

        phone['numverify'] = numverify(request_data.replace("+", ""))
        phone['getcontact'] = getcontact(request_data)
        
        return phone

    phone['getcontact'] = getcontact(request_data)
    phone['hlrlookup'] = HLRlookup(request_data, apilayerphone, hlruname, hlrpwd)
    phone['numverify'] = numverify(request_data.replace("+", ""))
    phone['truecaller'] = TrueCaller(request_data.replace("+91", ""))

    return phone