# python imports
import json
import re
from re import escape as reescape

# django imports
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# custom imports
from .models import Document, Sentence, Paragraphs


@csrf_exempt
def index(request):
    return render(request, 'index.html')


# ----- GRUPPE DOCUMENT LINKING -----

@csrf_exempt
def browse_documents(request):
    documents = Document.objects.all()
    context = {
        'documents': documents,
    }
    return render(request=request, template_name='./apps/doc_linking/browse_documents.html', context=context)


@csrf_exempt
def DocumentViewer(request, id):
    documents = Document.objects.all()
    document = Document.objects.get(id__exact=id)
    links_in_document = re.findall(r'<a[^<]*href="([^"]*)"[^>]*>([^<]*)<\/a', document.html_content)

    all_links = {}
    for link in links_in_document:
        link = list(link)
        link[1].replace('\n', ' ').replace('\r', '')
        link[1] = re.sub(' +', ' ', link[1])
        if len(re.sub(' ', '', link[1])) > 6:
            link[0].replace('\n', ' ').replace('\r', '')
            link[0] = re.sub(' +', ' ', link[0])
            all_links[link[0]] = link[1]

    context = {
        'document': document,
        'documents': documents,
        'all_links': all_links,
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
        filter_values["doc_name"] = Sentence.objects.all().values_list('doc_reference__title', flat=True)

    if (filter_values["start_date"] != None and filter_values["start_date"] != ""):
        start = int(filter_values["start_date"])
    else:
        start = Sentence.objects.all().values_list('date_iso', flat=True).order_by("date_iso").first()[:4]

    if (filter_values["end_date"] != None and filter_values["end_date"] != ""):
        end = int(filter_values["end_date"])
    else:
        end = Sentence.objects.all().values_list('date_iso', flat=True).order_by("date_iso").last()[:4]

    # erstellt Liste für alle Werte zwischen dem ausgewählten Start und End Jahr
    filter_values["date_range"] = [str(x) for x in list(range(int(start), int(end) + 1))]

    # filtert die Daten aus der Datenbank basierend auf den ausgewählten Filter Values
    data = Sentence.objects.filter(
        date_iso__regex='^({})'.format('|'.join(map(reescape, filter_values["date_range"]))),
        doc_reference__title__in=filter_values["doc_name"]
    ).order_by("date_iso")

    # extrahiert alle Dokumentennamen und Jahreszahlen aus der Datenbank, um sie als Optionen in die Datenbank zu schreiben
    distinct_doc_names = Sentence.objects.all().values_list('doc_reference__title', flat=True).distinct().order_by(
        "doc_reference__title")  # distinct values
    all_years = Sentence.objects.all().values_list('date_iso', flat=True).distinct().order_by("date_iso")

    distinct_years = []
    for year in all_years:
        if not year[0:4] in distinct_years:
            distinct_years.append(year[0:4])

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
