from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from .forms import Adsl_Form, Edit_Adsl_Form, Switch_Form, ServiceType_Form
from .models import AdslPort, SwitchPort
from interfaces.models import Router_model, Interface_model
from .reserve_port import FindReservePort
##########################################

def Services(request):    
    if request.method == 'POST':
        form = ServiceType_Form(request.POST)
        if form.is_valid():
            form.save()
            redirect("reserve:home") #redirect to any page you wish to send the user after registration 
    form = ServiceType_Form
    context = {'form':form}
    return render(request, 'service.html', context)
##########################################   
class Home(TemplateView):
  template_name = "home2.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 
##########################################
class Adsl(LoginRequiredMixin, View):
  template_name = "adsl.html"
  success_url = "reserve:reserveintlist"

##########################################
class Gateway(View):
  template_name = "gateway.html"
  context ={}
  all_routers = Router_model.objects.all()
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
      show_ints = 'showswitchport'+ '/' + request.POST["switches"]
      request.session['selected_switch']  = request.POST["switches"] ############ Router Name ##################
      return redirect(show_ints)
    else:
      self.context["gateway"] = False

    return render(request, self.template_name, self.context)
##########################################  

class Reserve_Int(LoginRequiredMixin, View):
  template_name = "reserve_int.html"
  success_url = reverse_lazy('interfaces:home')

  def get(self, request, pk):
    router_name = request.session.get("selected_switch")
    interface = Interface_model.objects.get(id = pk)
    int_date = date.today()
    int_user = request.user
    member = SwitchPort(Int=interface.Int_Name, 
                        Router=router_name, 
                        Date=int_date, 
                        Theauthor=int_user)
    form = Switch_Form (request.POST or None, instance = member)
    ctx = {'form': form}
    return render(request, self.template_name, ctx)

  def post(self, request, pk):
    form = Switch_Form (request.POST)
    if not form.is_valid():
      ctx = {'form': form}
      return render(request, self.template_name, ctx)
    # save form
    #frm = form.save(commite=False)
    form.save()
    return redirect(self.success_url)
  
##########################################
class Show_adslport(LoginRequiredMixin, View):
  template_name = "show_adslport.html"

  def get(self, request, pk):
    interface = AdslPort.objects.get(id = pk)
    ctx = {'interface': interface}
    return render(request, self.template_name, ctx)

##########################################
'''
class Show_switchport1(LoginRequiredMixin, View):
  template_name = "show_switchport.html"

  def get(self, request, pk):
    the_router = Router_model.objects.get(Name = pk)
    router_ints = the_router.Int_cross.all()
    ctx = {'router_name': pk,
           'interface': router_ints,
           'member_number': router_ints.count()}
    return render(request, self.template_name, ctx)
'''
class Show_switchport(LoginRequiredMixin, ListView):
    template_name = "show_switchport.html"
    context_object_name = 'interface'

    def get_queryset(self):
        the_router = get_object_or_404(Router_model, Name=self.kwargs["pk"])
        self.all_ints = the_router.Int_cross.all()
        return self.all_ints
    
    def get_context_data(self, **kwargs):
      # Call the base implementation first to get a context
      context = super().get_context_data(**kwargs)
      context["member_number"] = self.all_ints.count()
      context['router_name'] =  self.kwargs["pk"]
      return context
##########################################
class Show_adsl(generic.ListView):
    model = AdslPort
    template_name = 'show_adsl.html'
    ordering = ['Router']
    context_object_name = "members"
    
    def get_queryset(self):
       return super().get_queryset()
    
##########################################   
class Show_switch(generic.ListView):
    model = SwitchPort
    template_name = 'show_switch.html'
    ordering = ['Int']
    context_object_name = "members"
    
    def get_queryset(self):
       return super().get_queryset()
##########################################











class Reserve_int_list1(LoginRequiredMixin, View):
    def get(self, request):
        ml = Switch_Form.objects.all()
        ctx = {'members': ml, 'membernumber': ml.count()}
        return render(request, 'Reserve_int_list.html', ctx)
    ##############
class Reserve_int_list2(LoginRequiredMixin, TemplateView):
  template_name = "Reserve_int_list.html"
  
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    mymembers = Switch_Form.objects.all()
    number_fields = mymembers.count()
    ordered = mymembers.order_by("Router", "Int")  # show records sorted by Router name and interface name
    context = {'members':ordered, 'membernumber':number_fields}
    return context

##########################################
class Reserve_update(LoginRequiredMixin, View):
    model = Switch_Form
    success_url = reverse_lazy('reserve:reserveintlist')
    template = 'reserve_int.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = Switch_Form(instance=make)
        ctx = {'form': form}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = Switch_Form(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template, ctx)

        form.save()
        return redirect(self.success_url)

##########################################
class Update_adslport(LoginRequiredMixin, View):
  template_name = "show_adslport.html"
  success_url = "reserve:shoe-adsl"

  def get(self, request, pk):
    router_name = request.session.get("selected_switch")
    interface = AdslPort.objects.get(id = pk)
    int_date = date.today()
    int_user = request.user
    member = RouterPort(Int=interface.Int_Name, Router=router_name, Date=int_date, theauthor=int_user)

    form = Switch_Form (request.POST or None, instance = member)
    ctx = {'form': form}
    return render(request, self.template_name, ctx)

  def post(self, request, pk):
    form = Switch_Form (request.POST)

    if not form.is_valid():
      ctx = {'form': form}
      return render(request, self.template_name, ctx)
    
    # save form
    #frm = form.save(commite=False)
    form.save()
    return redirect(self.success_url)
##########################################
class MakeDelete(LoginRequiredMixin, View):
    model = Switch_Form
    success_url = reverse_lazy('interfaces:home')
    template = 'reserve_int.html'

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = Switch_Form(instance=make)
        ctx = {'make': make}
        return render(request, self.template, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        make.delete()
        return redirect(self.success_url)
##########################################
class Reserve_view(View):
  template_name = "reserve.html"
  
  def get(self, request):
    form = Reserve_Form ()
    return render(request, self.template_name, {'form': form})
 
  def post(self, request):
    #form = Reserve_Form (request.POST, instance= exist_reserve1)# update a previous data in database
    form = Reserve_Form (request.POST)
    gateway_IP = request.session.get("Gateway_ip")
    page_error =''
    if not form.is_valid():
      return render(request, self.template_name, {'form': form})
    
    myreserve = FindReservePort()
    gateway =                               myreserve.Return_gateway(gateway_IP)
    if gateway:
      gateway_obj =                         myreserve.Return_Gateway_obj()
      subport =                             myreserve.Return_subports()
      free_vlans =                          myreserve.Find_Vlan_inrange(2310, 2399)
      reservedports =                       myreserve.Return_reserved_ports()
      router_name =                         myreserve.Return_Routername()
      reserved_int =                        myreserve.Return_Intname()
      if router_name.find("9306")!= -1:
          reserved_int_new = reserved_int +'.'+ str(free_vlans[0])
      else:
        reserved_int_new = reserved_int +'.'+  myreserve.Return_PE() + str(free_vlans[0])
      
      my_Reserve = ReservePort(
        Peygiri =          form.cleaned_data['Peygiri'],
        Des =              form.cleaned_data['Des'],
        IP =               form.cleaned_data['IP'],
        Info =             form.cleaned_data['Info'],
        
        Service =          form.cleaned_data['Service'],
        Router =           myreserve.Return_Routername(),
        theauthor =        self.request.user,

        Encap =            myreserve.Return_Encap(),
        PE =               myreserve.Return_PE(),
        VLAN =             int(free_vlans[0]),
        Newint =           reserved_int_new,
        Date =             date.today(),
        Dayer =            False,
      )
      my_Reserve.save()
    else:     
      page_error = 'There is no Gateway' 
      messages.add_message(request, messages.SUCCESS, page_error) 
    
    return redirect('myint:reserveresult') 