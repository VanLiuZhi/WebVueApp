from django.shortcuts import render

# Create your views here.
from django.urls import path, include

urlpatterns = [
    path('api/', include('user.api')),
]