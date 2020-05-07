import requests,webbrowser
from io import BufferedReader

def reverseImg(img_path,img):
    try:
        #print("Enter the Image Path to Reverse : ")
        #img_path = str(img)
        searchUrl = 'https://www.google.co.in/searchbyimage/upload'
        multipart = {'encoded_image': (img_path, BufferedReader(img)), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']
        return fetchUrl

    except FileNotFoundError as e:
        return "File not Found"
    except:
        return "Something Went Wrong"
