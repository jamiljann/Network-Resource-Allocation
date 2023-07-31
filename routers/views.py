from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.template import loader
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from django.core.files.storage import FileSystemStorage
from .models import File_model
import os, datetime

from .models import RouterConfig_model
from .manage_files import Read_configfiles

########################################## 
def Import_file(request):
    if request.method == "POST":
      # if the post request has a file under the input name 'document', then save the file.
      request_file = request.FILES['selected_file'] if 'selected_file' in request.FILES else None
      if request_file:
        # save attached file
        fs = FileSystemStorage()
        file = fs.save(request_file.name, request_file)
        # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
        fileurl = fs.url(file)
    return render(request, 'import.html')
    
##########################################    
class Home(TemplateView):
  template_name = "home1.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 
##########################################
class Update_database(TemplateView):
  template_name = "update.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    read_config_files = Read_configfiles()
    read_config_files.Read_Router_Files()
    return 

##########################################
class Delete_database(TemplateView):
  template_name = "delete.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    read_config_files = Read_configfiles()
    read_config_files.Delete_Router_Files()
    return 
##########################################

class Router_list(ListView):
  template_name = "routerconfig_model_list.html"
  model = RouterConfig_model
  ordering = ["Name"]   # show records sorted by Name
  context_object_name = "members"

  def get_queryset(self):
      return super().get_queryset()
      

class Router_list2(ListView):
    model = RouterConfig_model
    template_name = "routerconfig_model_list.html"
    context_object_name = "members"
    

class Router_list1(TemplateView):
  template_name = "Router_list.html"
  
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    number_fields = RouterConfig_model.objects.all().count()
    members = RouterConfig_model.objects.all()
    ordered_members= members.order_by("Name")  # show records sorted by Router name and interface name
    context["members"] =   ordered_members
    context["numbers"] =   number_fields
    return context
##########################################

class Settings(TemplateView):
  template_name = "settings.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 