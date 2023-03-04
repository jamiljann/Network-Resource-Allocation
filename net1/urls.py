from django.contrib import admin
from django.urls import include, path

#from django.conf import settings
#from django.conf.urls.static import static



urlpatterns = [    
    path('',                include('members.urls')),
    path('myint/',          include('myint.urls')),
    path('admin/',          admin.site.urls),
    path('members/',        include('django.contrib.auth.urls')),
    path('members/',        include('members.urls')),
]
