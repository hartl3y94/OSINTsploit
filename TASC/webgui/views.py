from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from .modules.social.facebook import Facebook
from .modules.social.instagram import Instagram
from .modules.social.twitter import Twitter
from .modules.image.reverseimg import reverseImg
from .modules.social.locmap import loc

@csrf_exempt
def index(request):

  if request.method == 'GET':
    return render(request, 'index.html')

  if request.method == 'POST':
    query = str(request.POST['query'])
    query = query.split(":")

    if not len(query)<2:

      request_type = str(query[0])
      request_data = str(query[1])

      if request_type == 'facebook':

        fbdata = Facebook(request_data)
        return render(request, 'results.html',{'fbdata':fbdata})

      elif request_type == 'instagram':

          instadata = Instagram(request_data)
          if len(instadata['Location']) >0:
              gmap3=loc(instadata['Location'])
          else:
              instadata['Location']=None
              gmap3=None
          return render(request, 'results.html',{'instadata':instadata,'gmap3':gmap3})

      elif request_type == 'twitter':

          twitterdata = Twitter(request_data)
          return render(request, 'results.html',{'twitterdata':twitterdata})

    else:
      error = 'The requested Query is INVALID'
      return render(request, 'index.html', {'error':error})

    return render(request, 'index.html')

def modules(request):
    if request.method=="GET":
        return render(request, 'modules.html')
    elif request.method=="POST":
        url=reverseImg(str(request.FILES['input-b2']),request.FILES['input-b2'].file)
        if "https" in url:
            return redirect(url)
        else:
            return render(request, 'modules.html',{"Error":url})

def documentation(request):
  return render(request, 'documentation.html')

def about(request):
  return render(request, 'about.html')

@csrf_exempt
def settings(request):

  if request.method == 'GET':
   return render(request, 'settings.html')

  if request.method == 'POST':

    username = request.user.username

    user = User.objects.filter(username=username).first()

    if request.POST['hibpkey'] != '':
      user.profile.hibpkey = request.POST['hibpkey']

    if request.POST['hlrlookupkey'] != '':
      user.profile.hlrlookupkey = request.POST['hlrlookupkey']

    if request.POST['googleapikey'] != '':
      user.profile.googleapikey = request.POST['googleapikey']

    if request.POST['macapikey'] != '':
      user.profile.macapikey = request.POST['macapikey']

    if request.POST['ipstackkey'] != '':
      user.profile.ipstackkey = request.POST['ipstackkey']

    if request.POST['virustotalkey'] != '':
      user.profile.virustotalkey = request.POST['virustotalkey']

    user.profile.save()

    return render(request, 'settings.html')

@csrf_exempt
def logout(request):

  auth.logout(request)
  return HttpResponseRedirect("login")

@csrf_exempt
def login(request):

  if request.method == 'GET':
   return render(request, 'login.html')

  if request.method == 'POST':

    text = request.POST['policeid']

    password = request.POST['password']

    user = auth.authenticate(username=text, password=password)

    if user is not None:
      auth.login(request, user)
      #return render(request, 'dashboard.html', {'user':text})
      return redirect('index')

    else:
      return render(request, 'login.html', {'Auth':'False'})
