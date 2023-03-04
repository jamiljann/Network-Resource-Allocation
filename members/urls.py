from django.urls import include, path
from .import views


urlpatterns = [    
    path('',            views.login_user,            name="login"),
    path('login_user',  views.login_user,            name="login"),
    path('logout_user', views.logout_user,           name="logout"),  
]
