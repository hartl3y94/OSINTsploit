from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt

def index(request):
  return render(request, 'index.html')

def modules(request):
  return render(request, 'modules.html')

def documentation(request):
  return render(request, 'documentation.html')

def about(request):
  return render(request, 'about.html')

def settings(request):
  return render(request, 'settings.html')

def update_apikey(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.hibpkey = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

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