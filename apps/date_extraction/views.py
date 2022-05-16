from django.shortcuts import render
from django.http import JsonResponse
from .models import DateExtraction
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# only to render the page
@csrf_exempt
def index(request):

    data = DateExtraction.objects.all()
    data_object = DateExtraction.objects.all().values() 

    distinct_doc_names = DateExtraction.objects.all().values_list('DocName', flat=True).distinct().order_by("DocName") # distinct values
    # distinct_doc_names = DateExtraction.objects.all().values('DocName').distinct() # distinct objects 
    # {'DocName': 'Social Climate Fund'}
    # {'DocName': 'Proposal for a Directive on energy efficiency (rec'}

    distinct_years = DateExtraction.objects.all().values_list('IsoDate', flat=True).distinct().order_by("IsoDate")

    context = {
        "data": data, 
        "doc_names_filter": distinct_doc_names,
        "year_filter": distinct_years,
        "filter_data" : data_object,
    }

    return render(request, 'timeline.html', context)
