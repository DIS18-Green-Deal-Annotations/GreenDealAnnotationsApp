from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):

    table_absaetze = ['Eins', 'zwei', 'drei']

    context = {
        "tabellendaten": table_absaetze,
    }

    return render(request, 'index.html', context)