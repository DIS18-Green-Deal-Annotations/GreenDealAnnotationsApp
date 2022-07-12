from django.shortcuts import render
from .models import DateExtraction
from django.views.decorators.csrf import csrf_exempt
from re import escape as reescape
import json

# Create your views here.
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
    filter_values["date_range"] = [str(x) for x in list(range(int(start),int(end)+1))]

    # filtert die Daten aus der Datenbank basierend auf den ausgewählten Filter Values
    data = DateExtraction.objects.filter(
        isodate__regex= '^({})'.format('|'.join(map(reescape, filter_values["date_range"]))), docname__in=filter_values["doc_name"]
    )

    # extrahiert alle Dokumentennamen und Jahreszahlen aus der Datenbank, um sie als Optionen in die Datenbank zu schreiben
    distinct_doc_names = DateExtraction.objects.all().values_list('docname', flat=True).distinct().order_by("docname") # distinct values
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

    return render(request, 'timeline.html', context)
