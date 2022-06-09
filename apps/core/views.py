from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import html

from .models import HtmlCode


# @csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def test_page(request, id):
    code = HtmlCode.objects.filter(id=id).first()
    template = loader.get_template('test.html')
    print(type(code.html))
    context = {
        'code': {'html':code.html},
    }
    return HttpResponse(template.render(context, request))

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)