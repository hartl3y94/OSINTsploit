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
  path('documentation', views.documentation, name='documentation'),
  path('settings', views.settings, name='settings'),
  path('about', views.about, name='about'),
  path('logout', views.logout, name='logout'),
  path('modules', views.modules, name='modules'),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)