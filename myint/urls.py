from django.urls import path, include
from . import views
from django.views.generic.base import TemplateView # new

urlpatterns = [
    path('home',            views.Home.as_view(),                     name='home'),
    path('search',          views.search,                             name='search'),
    path('report',          views.Report.as_view(),                   name='report'),

    path('interfaces',      views.int_index.as_view(),                name='intindex'),
    path('routerlist',      views.Router_index.as_view(),             name='routerlist'),
    path('routerints/<str:id>',     views.Router_Ints_index,          name='routerints'),
    path('IPs',             views.IP_index.as_view(),                 name='ipindex'),

    path('reserve',         views.Reserve_view.as_view(),             name='reserve'),
    path('reservelist',     views.Reserve_index.as_view(),     name='reservelist'),
    
    #path('reservedelete/<int:id>',   views.ReservedDeleteView.as_view(),     name='deletereserved'),
    path('reserveresult',   views.Reserve_result.as_view(),           name='reserveresult'),
    path('gateway',         views.Gateway.as_view(),                  name='gateway'),

    path('about/',                 views.about,                       name='about'),
    path('deletereserve/<int:id>', views.deletereserve,               name='deletereserved'),
    path('editreserve/<int:id>'  , views.editreserve,                 name='editreserve'),
    
    path('add',               views.add,                              name='add'),
    #path('trans',             views.trans,                            name='trans'),
    
]