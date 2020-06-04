from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler400,handler403,handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),   
    path("", include("webgui.urls")),
    
]

handler400 = 'webgui.views.bad_request_error'
handler403 = 'webgui.views.forbidden'
handler404 = 'webgui.views.page_not_found'
handler500 = 'webgui.views.server_error'