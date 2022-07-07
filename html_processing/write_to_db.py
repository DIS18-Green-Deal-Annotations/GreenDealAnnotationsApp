import os
import sys
from pathlib import Path

import django
from django.conf import settings

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append('./')
settings.configure(
    DJANGO_SETTINGS_MODULE='GreenDealAnnotations.settings',
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'GreenDealAnnotations/db.sqlite3',
        }
    },
)
django.setup()

from core.models import HtmlCode

def main():

    #os.environ['DJANGO_SETTINGS_MODULE'] = 'GreenDealAnnotations.settings._base'

    path = "./crawler/html/"

    files = os.listdir(path)
    for file in files:
        print(type(file))
        document_name = file.split('.')[0]
        print(document_name)
        with open(path + file, 'r') as fl:
            code = str(fl.read())
            # print("helloooooo: ",code)
            check_if_existing = HtmlCode.objects.filter(document=document_name).exists()
            print(check_if_existing)
            if check_if_existing == False:
                save = HtmlCode.objects.create(html=code, document=document_name)


if __name__ == '__main__':
    main()
