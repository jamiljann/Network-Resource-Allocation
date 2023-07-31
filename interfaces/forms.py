from django.forms import ModelForm
from .models import Router_model

##########################################
Service_types = [
    ('Internet', 'Internet'),
    ('Intranet', 'Intranet'),
    ('Sip Trunk', 'Sip Trunk'),
    ('MPLS', 'MPLS'),
]
#########################################
class Router_Form(ModelForm):
    class Meta:
        model = Router_model
        fields = '__all__'
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)