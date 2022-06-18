import re

from django.shortcuts import render
from django.template import loader
from django.urls import get_resolver
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import html

from .models import HtmlCode


# @csrf_exempt
def index(request):
    """
    This view returns index.html and reads all URLs from url dispatcher to generate automatic navigation.

    The variable "excludes" may include URL names, namely the last string after "/" in a URL, to be excluded from
    automatic navigation creation for paths that shouldn't be exposed to the user (like the route to robots.txt).
    """

    excludes = ['robots.txt', 'admin']
    url_patterns = get_resolver().url_patterns
    url_paths = {}

    for url in url_patterns:
        # matches URLs in the extracted pattern.
        # Note: "'.*'" won't work because urls using include extract like this:
        # ["'apps.date_extraction.urls'", "'GreenDealAnnotationsApp/apps/date_extraction/urls.py'", "'timeline/'"]
        pattern_for_url = re.compile(r"'[^']*'")
        url_content = re.findall(pattern_for_url, str(url))

        url_path = url_content[-1]  # see Note before which is the reasoning selecting -1 in case of multiple finds
        url_path = url_path[1:-1]  # matching include apostrophes which must be excluded

        pattern_for_title = re.compile(r"[^\/]*")
        url_title = re.findall(pattern_for_title, str(url_path))

        non_empty_url_title = [x for x in url_title if x]  # remove empty strings from list

        url_title = 'home' if len(non_empty_url_title) == 0 else str(non_empty_url_title[-1])
        # as index page has usually root url '/'; set this one to "home" else
        # get last path element as name, e.g. original path "/index/test/me" would finally return "me"

        if url_title not in excludes:
            url_paths[url_title] = "/" + url_path

    return render(request, 'index.html', {"url_paths": url_paths})

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