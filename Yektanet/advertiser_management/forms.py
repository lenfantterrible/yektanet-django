from django.forms import ModelForm, ValidationError
from .models import Ad 

class AdForm(ModelForm):
    class Meta:
        model = Ad
        fields = '__all__'
        exclude = ('views', 'clicks')

