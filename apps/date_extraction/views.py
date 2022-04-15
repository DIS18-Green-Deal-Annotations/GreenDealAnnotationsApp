from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

# only to render the page
def index(request):
    return render(request, 'timeline.html')
