from django.forms import ModelForm

from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        labels = {"date": "Date", "specialty": "Specialty",
                  "description": "Description", }
