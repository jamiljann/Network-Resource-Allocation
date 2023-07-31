from django.views.generic.base import TemplateView

##########################################
class Settings(TemplateView):
  template_name = "settings.html"

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)    
    return 
