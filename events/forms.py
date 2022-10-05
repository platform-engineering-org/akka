from datetime import date

from django.forms import ModelForm, widgets

from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            "date": "Date",
            "specialty": "Specialty",
            "description": "Description",
        }
        widgets = {
            "date": widgets.DateInput(
                format="%d-%m-%Y",
                attrs={
                    "type": "date",
                    "class": "datepicker",
                    "value": date.today().isoformat(),
                },
            )
        }
