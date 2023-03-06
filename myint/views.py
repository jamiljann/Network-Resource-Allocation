from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.views import View
from datetime import date
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.contrib import messages
from django.shortcuts import render,redirect

from .models import Interface, Router, IP_model, ReservePort, ReservePort1, ServiceType

from .reserve_port21 import FindReservePort
from .fill import Fill_database
from .forms import Reserve_Form, Edit_Reserved_Form

##########################################
class Reserve_index(TemplateView):
  template_name = "gatewayreserved_index.html"
  
  def get_context_data(self, **kwargs) :

    context = super().get_context_data(**kwargs)
    number_fields = ReservePort.objects.all().count()
    mymembers = ReservePort.objects.all()
    #ordered = mymembers.order_by("IP")  #Tartib namayesh bar asase Date
    context["members"] =        mymembers
    context["membernumber"] =   number_fields
    #context["memberordered"] =  ordered
   
    return context

##########################################

class Router_index(ListView):
  template_name = "router_index.html"
  model = Router
  ordering = ["Name"]   #Tartib namayesh bar asase...
  context_object_name = "members"

  def get_queryset(self):
      members = super().get_queryset()
      return members

########################################## 
def Router_Ints_index(request, id):
  template = loader.get_template('int_index.html')
  
  the_router = Router.objects.get(Name = id)
  router_ints = the_router.Int_cross.all()
  context = {
      'router_name': id,
      'members': router_ints, 
      }  
  return HttpResponse(template.render(context, request))

##########################################
@login_required
def add(request):
  template = loader.get_template('add.html')
  a = Fill_database()
  return HttpResponse(template.render({}, request))

##########################################
def about(request):
  template = loader.get_template('about.html')
  return HttpResponse(template.render({}, request))

##########################################

class Report(TemplateView):
  template_name = "report.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    #context["message"]= "Created By Seyedjamil Sabbaghifaragard."
    return 
##########################################

def search(request):
  template = loader.get_template('search.html') 
  
  if 'button_ID' in request.POST:
    myid = request.POST.get("input_User_ID").strip()
    try:
      mymembers = Interface.objects.filter(int_ID__contains= myid) 
      membernumber = mymembers.count()
    except:
      raise Http404()
    context = {
      'interfaces': mymembers,
      'membernumber': membernumber 
      }  
  elif 'button_des' in request.POST:
    myid = request.POST.get("input_des").strip()
    try:
      mymembers = Interface.objects.filter(Description__contains= myid)
      membernumber = mymembers.count() 
    except:
      raise Http404()
    context = {
      'interfaces': mymembers, 
      'membernumber': membernumber
      }  
  elif 'button_name' in request.POST:
    myid = request.POST.get("input_name").strip()
    try:
      mymembers = Interface.objects.filter(int_Name__contains= myid) 
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
      mymembers = Interface.objects.filter(IP__contains= myip)
      membernumber = mymembers.count() 
    except:
      raise Http404()
    context = {
      'interfaces': mymembers, 
      'membernumber': membernumber
      }  
      
  elif 'button_gateway' in request.POST:
    gateway_IP = request.POST.get("gateway_IP").strip()
    myreserve = FindReservePort()
    gateway = myreserve.Return_gateway(gateway_IP)
   
    if gateway:
      context = {
        'interfaces':  gateway, 
        #'router_name': myreserve.Return_Gateway_obj()   #Return_Router(),
        }  
    else:
      context = {
        'interfaces':  None,
      }
  elif 'button_shut' in request.POST:
    myselect = request.POST.get("selected")
    print(myselect)
    try:
      if myselect == "shut":
        mymembers1 = Interface.objects.filter(Int_type__contains= "Shut Down") 
        mymembers2 =  mymembers1.filter(int_ID__isnull= False ).exclude(int_ID = '') 
        mymembers =   mymembers2.exclude(int_ID = 'None').order_by("Router_Name")
        membernumber = mymembers.count()
      elif myselect == "uplink":
        mymembers = Interface.objects.filter(Int_type__contains= "IPOSS_Uplink") | Interface.objects.filter(Int_type__contains= "ISIS_UpLink") 
        #mymembers =  mymembers1.filter(Int_type__contains= "LoopBack")#.order_by("Router_Name")
        membernumber = mymembers.count()
    except:
      raise Http404()
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

def signin(request):
  if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("There was an error login in.....Try again."))
            return redirect('/')
  else:
    return render(request, 'authentication/login.html', {})

##########################################
def deletereserve(request, id):
  member = ReservePort.objects.get(Peygiri=id)
  member.delete()
  return HttpResponseRedirect(reverse('reservelist'))

##########################################
def editreserve(request, id):
  member = ReservePort.objects.get(Peygiri=id)
  form = Edit_Reserved_Form(request.POST or None, instance = member)
  if form.is_valid():
    form.save()
    messages.success(request, (' Your reservation has been saved successfully.'))
    return redirect('reservelist')
  else:
    messages.success(request, (' There was an error in your form.'))
    return render(request, "reserve_edit.html", {"form":form})
  return render(request, "reserve_edit.html", {"form":form})

##########################################
class Home(TemplateView):
  template_name = "home.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    context["message"]= "Created By Seyedjamil Sabbaghifaragard."
    return 
    
##########################################
class Reserve_result(TemplateView):
  template_name = "reserve_result.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)

    gateway_IP = self.request.session.get("Gateway_ip")
    print('---------------gateway_IP:', gateway_IP)
    myreserve = FindReservePort()
    gateway = myreserve.Return_gateway(gateway_IP)
    if gateway:
      last_VLAN = myreserve.Find_Vlan_inrange(2310, 2399)
      reservedports = myreserve.Return_reserved_ports()
      context["reservedports"]= reservedports
      return context 
    else:
      return None
     
##########################################

class Gateway(View):
  template_name = "gateway.html"

  def get(self, request):
    context ={}
    return render(request, self.template_name, context)
  #---------------------------------
  def post(self, request):
    context = {}
    input_gateway = request.POST["input_DSLAM_IP"]
    #if input_gateway:
    if len(input_gateway.split('.')) == 4:
      myreserve = FindReservePort()
      gateway =                               myreserve.Return_gateway(input_gateway)
      if gateway:
        free_vlans =                          myreserve.Find_Vlan_inrange(2310, 2399)
        gateway_obj =                         myreserve.Return_Gateway_obj()
        subport =                             myreserve.Return_subports()
        reservedports =                       myreserve.Return_reserved_ports()
    
        request.session['Gateway_ip'] =      input_gateway   

        context["gateway"] =      gateway_obj
        context["subport"] =      subport
        context["reserveport"] =  reservedports
        return render(request, self.template_name, context)
      else:
        return render(request, self.template_name, context)
    else:
      context["gateway"] = False
      return render(request, self.template_name, context)

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
    #router_name = request.session.get("Routername")
    if form.is_valid(): 
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
          #Int =              gateway_obj,
          theauthor =        self.request.user,

          Encap =            myreserve.Return_Encap(),
          PE =               myreserve.Return_PE(),
          VLAN =             int(free_vlans[0]),
          Newint =           reserved_int_new,
          Date =             date.today(),
          Dayer =            False,
        )

        my_Reserve.save()
        return redirect('reserveresult') 
      page_error = 'There is no Gateway'  
      return render(request, self.template_name, {'form': form})

##########################################
class IP_index(TemplateView):
  template_name = "ip_index.html"
  
  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    number_fields = IP_model.objects.all().count()
    mymembers = IP_model.objects.all()
    ordered = mymembers.order_by("IP","Mask")  #Tartib namayesh bar asase Date
    context["members"] =        ordered
    context["membernumber"] =   number_fields
    return context
##########################################
class int_index(TemplateView):
  template_name = "int_index.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    number_interfaces = Interface.objects.all().count()
    #ordered_interfaces = interface.objects.all().order_by("Int_type")
    mymembers = Interface.objects.all().values()
    context["members"] = mymembers
    context["Number_records"] = number_interfaces

    return context






















