from django.forms import ModelForm
from .models import Reading

class ReadingForm(ModelForm):
    class Meta:
        model = Reading
        fields = ['date', 'status']
        widgets = {
            'date': {'type': 'date'},
        }