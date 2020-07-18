from .hibp import HaveIbeenPwned
from .hunter import hunter
from .slideshare import SlideShare
from .emailrep import emailrep
from .ghostproject import ghostproject

def Email():

    email = {}

    if hunterkey == "":
        pass
    else:
        email['hibp'] = HaveIbeenPwned(request_data, hibpkey)

    if hunterkey == "":
            pass
    else:
        email['hunterio'] = hunter(request_data, hunterkey)

    if emailrepkey == "":
        pass
    else:
        email['emailrep'] = emailrep(request_data, emailrepkey)

    email['ghostdata'] = ghostproject(request_data)
    email['slideshare'] = SlideShare(request_data)

    return email