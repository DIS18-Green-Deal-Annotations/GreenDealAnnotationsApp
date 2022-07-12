from django.shortcuts import render

def TestView(request):

    context = {
        "test": 5,
    }

    return(render(request=request, template_name='index.html', context=context))