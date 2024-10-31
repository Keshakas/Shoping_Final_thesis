from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Labas, pasauli!")
    return render(request, template_name="index.html")