from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import EventForm, EventsForm


def event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/events/events")
    else:
        form = EventForm()

    return render(request, "events/event.html", {"form": form})


def events(request):
    context = {"form": EventsForm()}
    return render(request, "events/events.html", context=context)


def thanks(request):
    return HttpResponse("Thanks. Your event was submitted.")
