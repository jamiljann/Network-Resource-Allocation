from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse
from django.conf import settings
##########################################
class ReservePort1(models.Model):
  Router_Name =   models.CharField(max_length=50)
  newint =        models.CharField(max_length=50)
  Encapsulation = models.CharField(max_length=50)
  newID =         models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(99999999999)] )
  Description =   models.CharField(max_length=155)
  IP =            models.CharField(blank=True, max_length=35)
  VLAN =          models.IntegerField(validators = [MinValueValidator(2300), MaxValueValidator(2999)])
  PE_vlan =       models.CharField(blank=True, max_length=10)
  User_type =     models.CharField(max_length=20)
  Rdate =         models.DateField()
  Rinfo =         models.CharField(blank=True, max_length=25)
  Dayer =         models.BooleanField(default=False)
  author =        models.ForeignKey(User, null= True, on_delete= models.SET_NULL)

  def __str__(self):
    return f'{self.Router_Name}-{self.Description}'
########################################## 
class Router(models.Model):
    Name =                  models.CharField(max_length=50)
    Type =                  models.CharField(max_length=50)
    IP =                    models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
      return f'{self.Name}'
##########################################

class Interface(models.Model):
  Router_Name =     models.ForeignKey(Router, on_delete=models.CASCADE, related_name="Int_cross")
  int_Name =      models.CharField(max_length=50)
  Description =   models.CharField(blank=True, max_length=155)
  int_ID =        models.CharField(blank=True, max_length=15)
  IP =            models.CharField(blank=True, max_length=35)
  Profile =       models.CharField(blank=True, max_length=25)
  VPN =           models.CharField(blank=True, max_length=50)
  Encapsulation = models.CharField(blank=True, max_length=50)
  Int_type =      models.CharField(max_length=15)

  def __str__(self):
    return f'{self.int_Name}'
##################################

class ServiceType(models.Model):
  name = models.CharField(max_length=150)
  def __str__(self):
      return f'{self.name}'
##################################

class ReservePort(models.Model):
  Router =      models.CharField(max_length=60)#  models.ForeignKey(Router, on_delete=models.CASCADE)
  Newint =      models.CharField(max_length=60)
  Encap =       models.CharField(max_length=50)
  Peygiri =     models.IntegerField(primary_key=True, validators = [MinValueValidator(1000), MaxValueValidator(99999999999)])
  Des =         models.CharField(max_length=155)
  IP =          models.CharField(null = True, blank=True, max_length=35)
  VLAN =        models.IntegerField(validators = [MinValueValidator(2300), MaxValueValidator(2999)])
  PE =          models.CharField(blank=True, null=True, max_length=10)
  Service =       models.ForeignKey(ServiceType, null=True, on_delete= models.CASCADE)
  Date =        models.DateField()
  Dayer =       models.BooleanField(default=False)
  Info =        models.CharField(blank=True, max_length=25)
  theauthor =      models.ForeignKey(User, null = True, on_delete= models.CASCADE)

  def __str__(self):
    return f'{self.Router}------------{self.Des}'
##########################################

class IP_model(models.Model):
  IP =            models.CharField(max_length=15)
  Mask =          models.CharField(max_length=15)
  VRF =           models.CharField(max_length=15)
  Destination =   models.CharField(max_length=15, null = True)
  Router =        models.CharField(max_length=15)
  Int =             models.ForeignKey(Interface, on_delete= models.CASCADE)
  Parvande =      models.CharField(blank=True, max_length=11)
  Description =   models.CharField(max_length=155, null = True, default = ' ')
  Type =          models.CharField(max_length=10, null = True)# =Routed  or   =under_interface

  def __str__(self):
    return f'{self.IP}-----{self.Router}__{self.Int.int_Name}'
