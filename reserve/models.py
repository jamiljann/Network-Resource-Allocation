from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

##################################
class ServiceType(models.Model):
  name = models.CharField(max_length=150)
   # Shows up in the admin list
  def __str__(self):
      return f'{self.name}'
  
##################################
class SwitchPort(models.Model):
  Router =      models.CharField(max_length=60)
  Int =         models.CharField(max_length=60)
  Peygiri =     models.IntegerField(primary_key=True, validators = [MinValueValidator(1000), MaxValueValidator(99999999999)])
  Des =         models.CharField(max_length=155)
  IP =          models.CharField(null = True, blank=True, max_length=35)
  VLAN =        models.IntegerField(validators = [MinValueValidator(2300), MaxValueValidator(2999)])
  Service =        models.ForeignKey(ServiceType, null=True, on_delete= models.CASCADE)
  Date =        models.DateField()
  Info =        models.CharField(blank=True, max_length=25)
  Theauthor =      models.ForeignKey(User, null = True, on_delete= models.CASCADE)
  File =         models.CharField(max_length=60)
   # Shows up in the admin list
  def __str__(self):
    return f'{self.Router}------------{self.Des}'
##################################  

class AdslPort(models.Model):
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
  Theauthor =      models.ForeignKey(User, null = True, on_delete= models.CASCADE)
  File =         models.CharField(max_length=60)

  def __str__(self):
    return f'{self.Router}------------{self.Des}'