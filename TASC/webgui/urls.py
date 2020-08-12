from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  path('', views.index, name='index'),
  path("reports",views.viewreport,name="reports"),
  path("deletereport",views.deletereport,name="deletereport"),
  path('login', views.login, name='login'),
  path('media/json/<str:username>.json', views.media, name='media'),
  path('settings', views.settings, name='settings'),
  path('change_password', views.change_password, name='change_password'),
  path('tracker', views.tracker, name='tracker'),
  path('trackactivity', views.trackactivity, name='trackactivity'),
  path('apps', views.apps, name='apps'),
  path('viewcases', views.viewcases, name='viewcases'),
  path('reverseimage', views.reverseimage, name='reverseimage'),
  path('metadata', views.metadata, name='metadata'),
  path('heatmap', views.heatmap, name='heatmap'),
  path('cluster',views.cluster,name='cluster'),
  path('<str:template>/<str:username>', views.receivetrack, name='meme'),
  path('documentation', views.documentation, name='documentation'),
  path('logout', views.logout, name='logout'),
  path('facedetector', views.FaceDetector, name='facedetector'),
  path('supeciousdetector',views.SupeciousDetector,name="SupeciousDetector")
]

if settings.DEBUG==False:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  