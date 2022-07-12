from django.shortcuts import render
# Create your views here.
from apps.document_classification.models import DocumentClassification


def document_classification(request):
    data = DocumentClassification.objects.all()
    context = {
        "model": data,
        # "doc_names_filter": distinct_doc_names,
        # "year_filter": distinct_years,
        # "start_year": filter_values["start_date"],
        # "end_year": filter_values["end_date"],
        # "doc_name": json.dumps(list(filter_values["doc_name"])),
        # "length_docs": len(list(distinct_doc_names)),
        # "length_filter_docs": len((list(filter_values["doc_name"])))
    }

    return render(request, 'document_classification.html', context)