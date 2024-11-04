from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Labas, pasauli!")
    return render(request, template_name="index.html")

def resume(request):
    return render(request, template_name="resume.html")

def projects(request):
    return render(request, template_name="projects.html")

def contact(request):
    return render(request, template_name="contact.html")