"""
Scraper und Crawler hätten die Kapazität mit dem doc linking code zusammen
sowohl CELEX als auch COM IDs automatisch generiert in die DB zu schreiben.

Im Rahmen des Merge-Prozesses der Gruppen ist der am geringst invasive
Eingriff im gegebenen Zeitrahmen an dieser Stelle COM IDs "manuell"
durch folgendes Dict nachzutragen.
"""

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

from core.models import Document

def add_com_ids():
    celex_com_matching = {
        'CELEX_52021DC0550': 'COM(2021) 550 final',
        'CELEX_52021PC0557': 'COM(2021) 557 final',
        'CELEX_52021PC0561': 'COM(2021) 561 final',
        'CELEX_52021DC0560': 'COM(2021) 560 final',
        'CELEX_52021PC0571': 'COM(2021) 571 final',
        'CELEX_52021PC0567': 'COM(2021) 567 final',
        'CELEX_52021PC0552': 'COM(2021) 552 final',
        'CELEX_52021PC0568': 'COM(2021) 568 final',
        'CELEX_52021PC0564': 'COM(2021) 564 final',
        'COM_2021_555_FIN': 'COM(2021) 555 final',
        'CELEX_52021PC0558': 'COM(2021) 558 final',
        'CELEX_52021PC0562': 'COM(2021) 562 final',
        'CELEX_52021DC0572': 'COM(2021) 572 final',
        'CELEX_52021PC0554': 'COM(2021) 554 final',
        'CELEX_52021PC0563': 'COM(2021) 563 final',
        'CELEX_52021PC0559': 'COM(2021) 559 final',
        'CELEX_52021PC0556': 'COM(2021) 556 final',
        'COM_2021_556_FIN': 'COM(2021) 556 final (pdf)',
    }

    for celex_id, com_id in celex_com_matching.items():
        modify = Document.objects.get(eu_id__exact=celex_id)
        modify.com_id = com_id
        modify.save()

if __name__ == '__main__':
    add_com_ids()














