from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
]