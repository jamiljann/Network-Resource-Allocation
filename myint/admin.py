from django.contrib import admin
from . import models
from .models import ReservePort, IP_model, Interface, ServiceType, Router


class ReserveAdmin(admin.ModelAdmin):
    readonly_fields = ("VLAN", )

admin.site.register(models.Router)
admin.site.register(models.ServiceType)
admin.site.register(models.ReservePort)    
admin.site.register(models.IP_model)  
admin.site.register(models.Interface)
