from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse
from django.conf import settings
##########################################

class Router_model(models.Model):
    Name =                  models.CharField(max_length=50)
    Type =                  models.CharField(max_length=50)
    IP =                    models.CharField(max_length=50, null=True, blank=True)   
    
    def __str__(self):
      """ String for representing the Model object"""
      return f'{self.Name}'
##########################################

class Interface_model(models.Model):
  Router_Name =     models.ForeignKey(Router_model, on_delete=models.CASCADE, related_name="Int_cross")
  Int_Name =      models.CharField(max_length=50)
  Description =   models.CharField(blank=True, max_length=155)
  int_ID =        models.CharField(blank=True, max_length=15)
  IP =            models.CharField(blank=True, max_length=35)
  Profile =       models.CharField(blank=True, max_length=25)
  VPN =           models.CharField(blank=True, max_length=50)
  Encapsulation = models.CharField(blank=True, max_length=50)
  Int_type =      models.CharField(max_length=15)

  def __str__(self):
    return f'{self.Int_Name}'
##########################################

class Interface_config_model(models.Model):
  Router_Name =     models.ForeignKey(Router_model, on_delete=models.CASCADE)
  int_Conf =        models.CharField(max_length=550)