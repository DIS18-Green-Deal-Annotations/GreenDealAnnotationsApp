# Dokumentation für die Integration der HTML Dateien in Django

## **Bevor die folgenden 2 Schritte ausgeführt werden können, müssen zunächst folgende vorbereitende Schritte ausgeführt werden.**

1. Venv (Virtual Enviroment) installieren und aktivieren
    1. `python3 -m venv .venv`
    2. `source .venv/bin/activate`

2. Packages über die requirements.txt installieren
    - `pip install -r requirements.txt`

3. Django User für den Admin erstellen
    - `python manage.py createsuperuser`

4. Django Models Migrationen erstellen
    - `python manage.py makemigrations`
    
5. Django Migrationen anwenden
    - `python manage.py migrate`
    

## Im wesentlichen besteht die Integration der HTML Dateien aus zwei Schritten


### 1. HTML crawlen und verarbeiten (Muss nur ausgeführt werden, falls Dateien noch nicht im Ordner html* liegen oder nach neuen Dateien gecheckt werden soll)

Im ersten Schritt werden die HTML Dateien über den Crawler (von Gilles geschrieben) gezogen und in dem Ordner **html** abgelegt. Dabei wird ebendfalls direkt gecheckt, ob neue HTML Dateien verfübar sind, falls die HTML Dateien schon inital gezogen worden sind. Anschließend werden die HTML Dateien durch die Methoden im *com_linking package* so prozessiert, dass alle *reinen Text COM Referenzen* in den Fußnoten in Hyperlinks transformiert werden (Arbeit der Document-Linking Gruppe).


**Um diesen Schritt auszuführen muss einfach nur das script *get_and_process.py* ausgeführt werden**

*in dem Ordner crawler


### 2. HTML Dateien in Django integrieren

Im zweiten Schritt werden die prozessierten HTML Dateien in die SQLite Datenbank von Django integriert. Spezieller werden die Dateien in das Model **HTMLCode** der App **core** geschrieben. Dabei wird ebenfalls gecheckt, ob schon Dateien in der Datenbank vorhanden sind und falls nein werden alle (neuen) Dateien der Datenbank hinzugefügt.


**Um diesen Schritt auszuführen muss einfach nur das Script *write_to_db.py* ausgeführt werden**

## Abschließend folgende Schritte ausführen

6. Django Server starten
    - `python manage.py runserver`
    
7. Admin öffnen mit Userdaten aus Schritt 4
    - [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

8. Im Admin unter core **Html codes** öffnen

9. (Optional) Html Dateien im Test View an schauen
    - http://127.0.0.1:8000/core/test/#beliebige_id_aus_HtmlCode_Table#/

    
