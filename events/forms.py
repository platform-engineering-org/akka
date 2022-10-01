from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["date", "description", ]
        labels = {'date': "Date", "description": "Description", }
