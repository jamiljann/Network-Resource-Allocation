from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings
#####################################
app_name = 'routers'

urlpatterns = [
    path('home',               views.Home.as_view(),                     name='home'),
    path('update',             views.Update_database.as_view(),          name='update'),
    path('list',               views.Router_list.as_view(),              name='list'),
    path('delete',             views.Delete_database.as_view(),          name='delete'),
    path('settings',           views.Settings.as_view(),                 name='settings'),

    path('import',             views.Import_file,                        name='importfile'),
]
