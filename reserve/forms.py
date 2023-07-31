from django.forms import ModelForm
from django import forms
from interfaces.models import Router_model
from .models import AdslPort, SwitchPort, ServiceType
#########################################

class ServiceType_Form(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = '__all__'
#########################################

class Adsl_Form(forms.ModelForm):
    class Meta:
        model = AdslPort
        exclude = ['theauthor', 'Date', 'Router', 'Encap', 'PE', 'VLAN', 'Newint', 'Dayer']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            "Router":"Router Name",
            "Newint":"New Interface",
            "Encap":"Encapsulation",
            "Peygiri":"New ID",
            "Des":"New Description",
            "IP":"New IP",
            "VLAN":"Vlan",
            "Date":"Date",
            "Info":"More Info",
            "Theauthor":"Creator",
            "File":"Attach File",
        }
        help_texts = {
               'IP': '(optional)'
            }
        error_messages={
            "newID":{
                "required":"You must assign a new ID to this new user.",
                "max_length": "Please enter a 12 digit length number for ID."
            },
        }
        widgets = {
            'Info': forms.Textarea(attrs={'cols': 20, 'rows': 1})
        }
    
#########################################
class Edit_Adsl_Form(forms.ModelForm):
    class Meta:
        model = AdslPort
        #fields = '__all__'
        exclude = ['Theauthor', 'Date']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            "Router":"Router Name",
            "Newint":"New Interface",
            "Encap":"Encapsulation",
            "Peygiri":"Customer ID",
            "Des":"Customer Description",
            "IP":"Customer IP",
            "VLAN":"Vlan",
            "Date":"Date",
            "Info":"More Info",
            "Theauthor":"Creator",
            "File":"Attach File",
        }
        help_texts = {
               'IP': '(optional)',
               'PE': '(optional)',
            }
        error_messages={
            "Peygiri":{
                "required":"You must assign a new ID to this new user.",
                "max_length": "Please enter an 11 digit length number for ID."
            },
        }
        widgets = {
            'Info': forms.Textarea(attrs={'cols': 20, 'rows': 2})
        }

#########################################
   
class Switch_Form(forms.ModelForm):
    #file1 = forms.FileField(required=False, label='File1 to upload ...')
    #upload_file_name = "myfile1"

    class Meta:
        model = SwitchPort
        #fields = '__all__'
        exclude = ['Theauthor', 'Date', 'File']
  
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            "Router":"Router Name",
            "Int":"Physical Interface",
            "Peygiri":"Customer ID",
            "Des":"Customer Description",
            "IP":"Customer IP",
            "VLAN":"Input a New Vlan",
            "Service":"Select Service Type",
            "Date":"Date",
            "Info":"More Info",
            "theauthor":"The Creator",
            "File":"Attach File",
        }
        help_texts = {
               'IP': '(optional)'
            }
        error_messages={
            "Peygiri":{
                "required":"You must assign a new ID to this new user.",
                "max_length": "Please enter an 11 digit length number for ID."
            },
        }
        widgets = {
            'Info': forms.Textarea(attrs={'cols': 20, 'rows': 1})
        }