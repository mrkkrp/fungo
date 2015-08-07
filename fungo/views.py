from django.shortcuts import render
from django.http import HttpResponse

# Views

def index (request):
    context_dict = {'boldmessage': "I'm bold message from the context."}
    return render(request, 'fungo/index.html', context_dict)

def about (request):
    return HttpResponse(
"Fungo says here is about page! <a href='/fungo/'>Go back to main page</a>.")
