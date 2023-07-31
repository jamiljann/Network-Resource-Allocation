from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader

from .models import Router_model, Interface_model, Interface_config_model
from  routers.models import RouterConfig_model
from .make_interfaces import Create_router_interfaces

##########################################
class Update_database(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs) 
    selected_date = '2022-06-25'   
    all_files = RouterConfig_model.objects.all()
    specific_time_files = all_files.filter(Filedate = selected_date)   # Select config files on the specific time
    
    if specific_time_files:
      for item in specific_time_files:
        print('+++++++++++ Router Name:',item.Name)
        cri = Create_router_interfaces()
        cri.Create_interfaces_config(item)
    else:
      print('There isnt any config file in this date.')
    return 

##########################################
class Delete_database(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    read_config_files = Create_router_interfaces()
    read_config_files.Delete_previous_routers()
    return 
##########################################
class Int_list(TemplateView):
  template_name = "int_list.html"
  
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    number_fields = Interface_model.objects.all().count()
    members = Interface_model.objects.all()
    ordered_members= members.order_by("Router_Name")  # show records sorted by Router name and interface name
    context["members"] =   ordered_members
    context["numbers"] =   number_fields
    return context
##########################################
class Router_list(TemplateView):
  template_name = "router_list.html"
  
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    number_fields = Router_model.objects.all().count()
    members = Router_model.objects.all()
    #ordered_members= members.order_by("Name")  # show records sorted by Router name and interface name
    context["members"] =   members #ordered_members
    context["numbers"] =   number_fields
    return context
##########################################
class Settings(TemplateView):
  template_name = "settings.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 
########################################## 
class Home(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 
  
##########################################
##########################################
##########################################

class Report(TemplateView):
  template_name = "report.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    return 
##########################################
def Search(request):
  template = loader.get_template('search.html') 
  
  if 'button_ID' in request.POST:
    myid = request.POST.get("input_User_ID").strip()
    try:
      mymembers = Interface_model.objects.filter(int_ID__contains= myid) 
      membernumber = mymembers.count()
    except:
      raise Http404("Given query not found....")
    context = {
      'interfaces': mymembers,
      'membernumber': membernumber 
      }  
  elif 'button_des' in request.POST:
    myid = request.POST.get("input_des").strip()
    try:
      mymembers = Interface_model.objects.filter(Description__contains= myid)
      membernumber = mymembers.count() 
    except:
      raise Http404("Given query not found....")
    context = {
      'interfaces': mymembers, 
      'membernumber': membernumber
      }  
  elif 'button_name' in request.POST:
    myid = request.POST.get("input_name").strip()
    try:
      mymembers = Interface_model.objects.filter(Int_Name__contains= myid) 
      membernumber = mymembers.count()
    except:
      raise Http404()
    context = {
      'interfaces': mymembers, 
      'membernumber': membernumber
      }  
  elif 'button_IP' in request.POST:
    myip = request.POST.get("input_IP").strip()
    try:
      mymembers = Interface_model.objects.filter(IP__contains= myip)
      membernumber = mymembers.count() 
    except:
      raise Http404("Given query not found....")
    context = {
      'interfaces': mymembers, 
      'membernumber': membernumber
      }  
  else:
    context = {
      'interfaces': None, 
      }  
  return HttpResponse(template.render(context, request)) 
 
##########################################
'''
class Gateway(View):
  template_name = "Find_reserve.html"
  context ={}
  all_routers = Router.objects.all()
  context["routers"] = all_routers

  def get(self, request): 
    return render(request, self.template_name, self.context)
  #---------------------------------
  def post(self, request):
    if 'input_DSLAM_IP' in request.POST:
      input_gateway = request.POST["input_DSLAM_IP"]
      if len(input_gateway.split('.')) == 4:
        myreserve = FindReservePort()
        gateway =                               myreserve.Return_gateway(input_gateway)
        if gateway:
          free_vlans =                          myreserve.Find_Vlan_inrange(2310, 2399)
          gateway_obj =                         myreserve.Return_Gateway_obj()
          subport =                             myreserve.Return_subports()
          reservedports =                       myreserve.Return_reserved_ports()
      
          request.session['Gateway_ip'] =      input_gateway  

          self.context["gateway"] =      gateway_obj
          self.context["subport"] =      subport
          self.context["reserveport"] =  reservedports
          return render(request, self.template_name, self.context)
        else:
          return render(request, self.template_name, self.context)
      else:
        self.context["gateway"] = False
        return render(request, self.template_name, self.context)
        #return Http404
    elif 'switches' in request.POST:
      print("Selected Switch for Reserve= ",  request.POST["switches"])
      show_ints = 'selectrouterints'+ '/' + request.POST["switches"]
      request.session['selected_switch']  = request.POST["switches"] ############ Router Name ##################
      return redirect(show_ints)
    else:
      self.context["gateway"] = False

    return render(request, self.template_name, self.context)
'''
##########################################
def about(request):
  template = loader.get_template('about.html')
  return HttpResponse(template.render({}, request))
