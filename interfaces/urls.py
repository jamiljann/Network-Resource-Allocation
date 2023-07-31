from django.urls import path, include
from . import views
#####################################
app_name = 'interfaces'

urlpatterns = [
    path('home',               views.Home.as_view(),                     name='home'),
    path('update',             views.Update_database.as_view(),          name='update'),
    path('delete',             views.Delete_database.as_view(),          name='delete'),
    path('intlist',            views.Int_list.as_view(),                 name='int_list'),
    path('routerlist',         views.Router_list.as_view(),              name='router_list'),
    path('settings',           views.Settings.as_view(),                 name='settings'),

    path('search',          views.Search,                             name='search'),
    path('report',          views.Report.as_view(),                   name='report'),
    path('about/',                 views.about,                       name='about'),
]