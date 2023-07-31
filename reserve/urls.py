from django.urls import path, include
from . import views
#####################################
app_name = 'reserve'

urlpatterns = [
    path('gateway',                   views.Gateway.as_view(),           name='gateway'),
    path('reserveadsl',               views.Adsl.as_view(),              name='reserve-adsl'),
    path('reserveint/<str:pk>',       views.Reserve_Int.as_view(),       name='reserve-int'),
    path('showadsl',                  views.Show_adsl.as_view(),         name='show-adsl'),
    path('showswitch',                views.Show_switch.as_view(),       name='show-switch'),
    path('showadslport/<int:pk>',     views.Show_adslport.as_view(),     name='show-adslport'),
    path('showswitchport/<str:pk>',   views.Show_switchport.as_view(),   name='show-switchport'),
    path('services',                  views.Services,          name='services'),
    
    path('reserve_update/<int:pk>',           views.Reserve_update.as_view(),    name='reserve_update'),
       
    path('home',               views.Home.as_view(),                     name='home'),
    path('delete',             views.MakeDelete.as_view(),               name='delete'),
]