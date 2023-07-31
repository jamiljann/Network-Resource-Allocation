from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse
from django.conf import settings
##########################################
class RouterConfig_model(models.Model):
  Name =                models.CharField(max_length=50)
  Showrun =             models.CharField(max_length=5000)
  Filedate =            models.DateField()
  #Type =                models.CharField(max_length=50, null=True, blank=True)
  #IP =                  models.CharField(max_length=50, null=True, blank=True)

  def __str__(self):
    return f'{self.Name}-{self.Filedate}'
########################################## 

class File_model(models.Model):
    file = models.FileField()

    def __str__(self):
        return self.file.name