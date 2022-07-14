import os
import sys
from pathlib import Path

import django
from django.conf import settings

from date_extraction import init_doc_obj

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append('./')
# settings.configure(
#     DJANGO_SETTINGS_MODULE='GreenDealAnnotations.settings',
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': BASE_DIR / 'GreenDealAnnotations/db.sqlite3',
#         }
#     },
# )
django.setup()

from core.models import TABLE_CATEGORIES, TABLES

def main():
    table_path = r"../crawler/tables_html/"
    categories_path = r"./categories.txt"
    docs_and_tables = {}
    DocID = 0
    for file in os.listdir(table_path):
        Filename_full = os.fsdecode(file)
        Filename_splitted = Filename_full.split(" final_")
        TableNr = Filename_splitted[1].split(".")[0] # Important
        ComNr = Filename_splitted[0].strip() # Important
        TableContentHTML = open(table_path+Filename_full, "r", encoding="UTF-8") # Important
        if not ComNr in docs_and_tables.keys():
            docs_and_tables[ComNr] = [TableNr]
            DocID += 1 # Important
        else:
            docs_and_tables[ComNr].append(TableNr)
        Filename = table_path + Filename_full # Important
        TABLES.objects.create(
            ComNr = ComNr,
            DocID = DocID,
            TableNr = TableNr,
            Filename = Filename,
            TableContentHTML = TableContentHTML
        )
    with open(categories_path, "r") as categories_file:
        lines = categories_file.read().splitlines()
        CatID = 0
        for category in lines:
            CatID += 1
            TABLE_CATEGORIES.objects.create(
                    Category = category,
                    CatID = CatID
                )


if __name__ == '__main__':
    main()
