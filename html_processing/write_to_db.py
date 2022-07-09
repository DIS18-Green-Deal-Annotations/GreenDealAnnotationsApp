import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

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

from core.models import Document

def main():

    #os.environ['DJANGO_SETTINGS_MODULE'] = 'GreenDealAnnotations.settings._base'

    path = "./crawler/html/"

    # Liste der Date Extraction Gruppe ziehen:
    docs_meta_data = init_doc_obj()

    list_of_manually_added_pdfs = ['CELEX_52021PC0556', 'COM_2021_556_FIN']

    files = os.listdir(path)
    for file in files:
        print(type(file))
        document_name = file.split('.')[0]
        print(document_name)
        with open(path + file, 'r') as fl:
            code = str(fl.read())
            check_if_existing = Document.objects.filter(eu_id=document_name).exists()
            print(check_if_existing)

            if not check_if_existing:
                if len(code) > 10:
                    # some documents are not html; only pdf. Hence the crawler returns empty documents
                    # in this case we create a limited object will create the 3 objects later on in this code manually
                    soup = BeautifulSoup(code)
                    right_doc = soup.find("p", {"class": "Titreobjet_cp"})
                    right_doc_title = right_doc.text.lstrip().rstrip()
                    right_doc_title = right_doc_title.replace(u'\xa0', ' ')
                    right_doc_title = right_doc_title.replace('&nbsp;', ' ')
                    print(right_doc_title)
                    title = ''  # title of the document on official website
                    subtitle = ''  # title of the doc in html -> usually document title or a subtitle
                    scope = ''
                    url = ''  # URL to original html document
                    publish_date = ''
                    doc_type = ''
                    counter = 0
                    for doc in docs_meta_data:
                        if doc.titreobject == right_doc_title:
                            print('right_doc_found')
                            print('it was document: ' + str(counter))
                            title = doc.name
                            subtitle = doc.titreobject
                            scope = doc.typedudocument
                            url = doc.url
                            doc_type = doc.type
                            publish_date = doc.date
                        counter += 1

                    save = Document.objects.create(
                        title=title,
                        html_content=code,
                        eu_id=document_name,
                        subtitle=subtitle,
                        scope=scope,
                        url=url,
                        file_type=doc_type,
                        publish_date=datetime.strptime(publish_date, '%Y-%m-%d'),
                    )
                else:

                    if document_name == list_of_manually_added_pdfs[0]:
                        save = Document.objects.create(
                            title='Proposal for a REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL amending Regulation (EU) 2019/631 as regards strengthening the CO2 emission performance standards for new passenger cars and new light commercial vehicles in line with the Union’s increased climate ambition',
                            html_content='',
                            eu_id='CELEX_52021PC0556',
                            subtitle='amending Directive 2003/87/EC establishing a system for greenhouse gas emission allowance trading within the Union, Decision (EU) 2015/1814 concerning the establishment and operation of a market stability reserve for the Union greenhouse gas emission trading scheme and Regulation (EU) 2015/757',
                            scope='DIRECTIVE OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL',
                            url='https://ec.europa.eu/info/sites/default/files/revision-eu-ets_with-annex_en_0.pdf',
                            file_type='pdf',
                            publish_date=datetime.strptime('2021-07-14', '%Y-%m-%d'),
                        )
                    elif document_name == list_of_manually_added_pdfs[1]:
                        save = Document.objects.create(
                            title='Proposal for a REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL amending Regulation (EU) 2019/631 as regards strengthening the CO2 emission performance standards for new passenger cars and new light commercial vehicles in line with the Union’s increased climate ambition',
                            html_content='',
                            eu_id='COM_2021_556_FIN',
                            subtitle='amending Regulation (EU) 2019/631 as regards strengthening the CO2 emission performance standards for new passenger cars and new light commercial vehicles in line with the Union’s increased climate ambition',
                            scope='REGULATION OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL',
                            url='https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52021PC0556&from=EN',
                            file_type='pdf',
                            publish_date=datetime.strptime('2021-07-14', '%Y-%m-%d'),
                        )
                    else:
                        print('Missing CELEX ID Document for manual entry: ' + str(document_name))


if __name__ == '__main__':
    main()
