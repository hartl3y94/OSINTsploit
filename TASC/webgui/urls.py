from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path('login', views.login, name='login'),
  path('modules', views.modules, name='modules'),
  path('media/json/<str:username>.json', views.media, name='media'),
  path('settings', views.settings, name='settings'),
  path('change_password', views.change_password, name='change_password'),
  path('tracker', views.tracker, name='tracker'),
  path('reverseimage', views.reverseimage, name='reverseimage'),
  path('<str:template>/<str:username>', views.receivetrack, name='meme'),
  path('documentation', views.documentation, name='documentation'),
  path('logout', views.logout, name='logout'),
]

if settings.DEBUG==False:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  