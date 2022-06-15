import os, sys
sys.path.append('./')
os.environ['DJANGO_SETTINGS_MODULE'] = 'GreenDealAnnotations.settings._base'
import django
django.setup()
from apps.core.models import HtmlCode

if __name__ == '__main__':


    path = "./html_processing/crawler/html/"

    files = os.listdir(path)
    for file in files:
        print(type(file))
        document_name = file.split('.')[0]
        print(document_name)
        with open(path + file, 'r') as fl:
            code = str(fl.read())
            #print("helloooooo: ",code)
            check_if_existing = HtmlCode.objects.filter(document=document_name).exists()
            print(check_if_existing) 
            if check_if_existing == False:
                save = HtmlCode.objects.create(html=code, document=document_name)