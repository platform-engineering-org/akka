from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import EventForm
from .models import Event


def event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/events/thanks')
    else:
        form = EventForm()

    return render(request, 'events/event.html', {'form': form})


def events(request):
    form = Event.objects.all()
    context = {'form': form}
    return render(request, 'events/events.html', context)


def thanks(request):
    return HttpResponse("Thanks. Your event was submitted.")
