from django.forms import ModelForm
from .models import AppealPoint

class AppealPointForm(ModelForm):
    class Meta:
        model  = AppealPoint
        fields = ['task','process','result','force']
