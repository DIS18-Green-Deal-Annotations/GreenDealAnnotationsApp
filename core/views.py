# python imports
import json
import re
from re import escape as reescape

# django imports
from django.shortcuts import render
from django.urls import get_resolver
from django.views.decorators.csrf import csrf_exempt

# custom imports
from .models import HtmlCode, DateExtraction


@csrf_exempt
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


# ----- GRUPPE DOCUMENT LINKING -----


@csrf_exempt
def DocumentViewer(request, id):
    code = HtmlCode.objects.get(id__exact=id)
    context = {
        'code': {'html': code.html}
    }

    return render(request=request, template_name='./apps/doc_linking/document_viewer.html', context=context)


# ----- GRUPPE DATE EXTRACTION -----


@csrf_exempt
def timeline(request):
    # zieht sich die übergebenen Filter Values aus der Query
    filter_values = {}
    filter_values["doc_name"] = request.GET.get("doc_name")
    filter_values["start_date"] = request.GET.get("start_date")
    filter_values["end_date"] = request.GET.get("end_date")

    # sollten Filter Kategorien nicht ausgewählt worden sein, wird auf Defaults zurückgegriffen
    if (filter_values["doc_name"] != None and filter_values["doc_name"] != ""):
        filter_values["doc_name"] = filter_values["doc_name"].split(",")
    else:
        filter_values["doc_name"] = DateExtraction.objects.all().values_list('docname', flat=True)

    if (filter_values["start_date"] != None and filter_values["start_date"] != ""):
        start = int(filter_values["start_date"])
    else:
        start = DateExtraction.objects.all().values_list('isodate', flat=True).order_by("isodate").first()[:4]

    if (filter_values["end_date"] != None and filter_values["end_date"] != ""):
        end = int(filter_values["end_date"])
    else:
        end = DateExtraction.objects.all().values_list('isodate', flat=True).order_by("isodate").last()[:4]

    # erstellt Liste für alle Werte zwischen dem ausgewählten Start und End Jahr
    filter_values["date_range"] = [str(x) for x in list(range(int(start), int(end) + 1))]

    # filtert die Daten aus der Datenbank basierend auf den ausgewählten Filter Values
    data = DateExtraction.objects.filter(
        isodate__regex='^({})'.format('|'.join(map(reescape, filter_values["date_range"]))),
        docname__in=filter_values["doc_name"]
    )

    # extrahiert alle Dokumentennamen und Jahreszahlen aus der Datenbank, um sie als Optionen in die Datenbank zu schreiben
    distinct_doc_names = DateExtraction.objects.all().values_list('docname', flat=True).distinct().order_by(
        "docname")  # distinct values
    distinct_years = DateExtraction.objects.all().values_list('isodate', flat=True).distinct().order_by("isodate")

    context = {
        "data": data,
        "doc_names_filter": distinct_doc_names,
        "year_filter": distinct_years,
        "start_year": filter_values["start_date"],
        "end_year": filter_values["end_date"],
        "doc_name": json.dumps(list(filter_values["doc_name"])),
        "length_docs": len(list(distinct_doc_names)),
        "length_filter_docs": len((list(filter_values["doc_name"])))
    }

    return render(request, './apps/date_extraction/timeline.html', context)
