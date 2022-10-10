from datetime import date

from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        labels = {
            "date": "Date",
            "specialty": "Specialty",
            "description": "Description",
        }
        widgets = {
            "date": forms.widgets.DateInput(
                format="%d-%m-%Y",
                attrs={
                    "type": "date",
                    "class": "datepicker",
                    "value": date.today().isoformat(),
                },
            )
        }


class EventsForm(forms.Form):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
