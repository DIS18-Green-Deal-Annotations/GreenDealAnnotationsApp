# GreenDealAnnotationsApp

# GEÄNDERTE README BEACHTEN:

## Installation

Für Entwicklung:
`pip install -r requirements/dev.txt`
Für Produktion:
`pip install -r requirements/dev.txt`

Erklärung:
Alle benötigten Pakete sind im Ordner `requirements` hinterlegt.
In der Datei `_base.txt` weren alle Pakete eingetragen die immer benötigt werden.
Über `dev.txt` werden alle Pakete aus `_base.txt` installiert sowie Pakete die nur während der Entwicklung, 
also beispielsweise Testsuites, revelant sind.
Analog werden über `prod.txt` alle Pakete aus `_base.txt` installiert sowie Pakete die nur während 
des Deployments revelant sind.

## Datenbank mit Daten befüllen

Die Datei `setup.py` kann ausgeführt werden um die Skripte aller Gruppen zu starten die die Datenbank automatisch mit Daten befüllen.
Vorher muss zusätzlich der Befehl `python -m spacy download en_core_web_sm` ausgeführt werden.

## Arbeiten mit Django

Der Ordner `core` enhält alle Dateien zum Arbeiten mit Django.
Einzelne Apps pro Gruppe gibt es nicht mehr. Hier wurden alle Dateien zusammengefasst.

Alle URLs sind jetzt in der gemeinsamen `GreenDealAnnotations/urls.py` Datei. Einzelne Dateien pro Gruppe gibt es nicht mehr.

Im Ordner `GreenDealAnnotations/templates` liegen alle HTML-Dateien unserer Seiten.

Der Ordner `GreenDealAnnotations/static` enthält alle statischen Dateien der Website, also CSS, JavaScript, und Bilder.
Wie diese in HTML eingebunden werden kann man sich gut bei der Date Extraction Gruppe aus der Datei `GreenDealAnnotations/templates/apps/date_extraction/timeline.html` abgucken.

## Tests und Testdaten für DB

Dateien die mit `test_` starten werden von Django als Tests erkannt.
Diese können mit `manage.py test` ausgeführt werden.

Ein Beispiel aus der Dokumentation:
```
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    def setUp(self):
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
```


### Skript für Testdaten manuell erstellen
Analog kann auch ein Skript erstellt werden um Testdaten zu generieren.

Beispielsweise so könnte ein Skript für eure Gruppe aussehen um für eure Models Daten zu generieren:

```
from mygroup.models import MyModel

def setupTestDataForMyModel():
    MyModel.objects.create(name="..." ...)
```

(bitte sobald erstellt in der Readme erwähnen damit andere Gruppen wissen wie sie euer Skript für Testdaten starten können)

### Skript für Testdaten automatisiert erstellen

Einfacher wäre es mit "fixtures" zu arbeiten.
Wenn ihr Daten in der DB erstellt wurden kann mit `manage.py dumpdata` eine fixtures-Datei, also ein Export erstellt werden.

Anschließen muss im Ordner der jeweiligen App ein Ordner "fixtures" erstellt werden.
Die Datei/en werden dort platziert.

Ein Beispiel aus der Django Dokumentation wenn eine fixture mit Namen `bird` generiert wurde:

```
from django.test import TestCase
from myapp.models import Animal

class AnimalTestCase(TestCase):
    fixtures = ['birds']

    def setUp(self):
        # Test definitions as before.
        call_setup_methods()

    def test_fluffy_animals(self):
        # A test that uses the fixtures.
        call_some_test_code()
```

Abseits vom Erstellen/Starten von Tests bei den die Daten schon geladen wurden kann die Funktion auch genutzt werden
 um nur die Daten aus der fixture wieder in die DB zu überspielen:
`AnimalTestCase.setUp()`

(Hinweis: bevor Django die Daten in die DB spielt werden alle aktuellen Daten aus der DB entfernt!)
(Hinweis2: die implizit aufgerufene Funktion `setUpTestData()` gehört zur Django-Klasse `TestCase`)