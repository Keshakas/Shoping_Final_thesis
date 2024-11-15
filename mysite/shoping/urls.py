from django.urls import path, include


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resume/', views.resume, name='resume'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]