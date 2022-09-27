from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import EventForm


def event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = EventForm()

    return render(request, 'akka/event.html', {'form': form})


def thanks(request):
    return HttpResponse("Thanks. Your event was submitted.")
