from django import forms
from .models import ReservePort, Router
##########################################
#IP_types = [('Static', 'Static'),('Route', 'Route'),]

#class IP_Form(forms.ModelForm):
#    service_choice = forms.ChoiceField(
#        label = 'Select User Sevice ', 
#        widget=forms.Select,
#        choices= Service_types
#    )
#    class Meta:
#        model = ReservePort
##########################################
Service_types = [
    ('Internet', 'Internet'),
    ('Intranet', 'Intranet'),
    ('Sip Trunk', 'Sip Trunk'),
    ('MPLS', 'MPLS'),
]
#########################################
class Router_Form(forms.ModelForm):
    class Meta:
        model = Router
        fields = '__all__'
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
#########################################

class Reserve_Form(forms.ModelForm):
    class Meta:
        model = ReservePort
        exclude = ['theauthor', 'Date', 'Router', 'Encap', 'PE', 'VLAN', 'Int', 'Newint', 'Dayer']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            "Router":"Router Name",
            "Int":"Base Interface",
            "Newint":"New Interface",
            "Encap":"Encapsulation",
            "Peygiri":"Customer ID",
            "Des":"Customer Description",
            "IP":"Customer IP",
            "VLAN":"Vlan",
            "Date":"Date",
            "Info":"More Info",
            "theauthor":"Creator",
        }
        help_texts = {
               'IP': '(optional)'
            }
        error_messages={
            "newID":{
                "required":"You must assign a new ID to this new user.",
                "max_length": "Please enter a 10 digit length number for ID."
            },
        }
        widgets = {
            'Info': forms.Textarea(attrs={'cols': 20, 'rows': 1})
        }
    
#########################################
class Edit_Reserved_Form(forms.ModelForm):
    class Meta:
        model = ReservePort
        #fields = '__all__'
        exclude = ['theauthor', 'Date']
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        labels = {
            "Router":"Router Name",
            "Int":"Interface Name",
            "Newint":"New Interface",
            "Encap":"Encapsulation",
            "Peygiri":"Customer ID",
            "Des":"Customer Description",
            "IP":"Customer IP",
            "VLAN":"Vlan",
            "Date":"Date",
            "Info":"More Info",
            "theauthor":"Creator",
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
    
