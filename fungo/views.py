from django.shortcuts import render
from django.http import HttpResponse

# Views

def index (request):
    return HttpResponse("<a href='/fungo/about'>Fungo</a> says hello!")

def about (request):
    return HttpResponse(
"Fungo says here is about page! <a href='/fungo/'>Go back to main page</a>.")
