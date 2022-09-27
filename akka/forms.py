from django import forms


class EventForm(forms.Form):
    date = forms.DateField()
    description = forms.CharField(label='Description', max_length=100)
