# CHANGELOG
## kommentar von oliver 15.06.2022
- date_extraction als command eingefügt. Aufzurufen mit: 'npython manage.py date_extraction'
    - Info: Server muss dafür laufen
- daten werden noch mit eigenem crawler gecrawlt und in die django db geschrieben

## kommentar von oliver 15.04.2022:
- änderungen an apps/date_extraction
    - die timeline aus der date extraction gruppe übernommen
        - abrufbar unter: http://127.0.0.1:8000/timeline/
        - die timeline zieht ihre daten noch aus einer csv datei mit den vorher extrahierten sätzen (keine live scrapper daten)
    - neues modell der db hinzugefügt und mit testdaten gefüllt
        - spalten des modell lauten: DocName, DocSentence, DateLabel, IsoDate
- änderungen an apps/core
    - neu erstelltes mdell der admin page hinzugefügt (admin.py)
    - code in models.py auskommentiert, da dieser code zu fehlern geführt hat. wahrscheinlich is es noch code aus den schulungsterminen?
- urls.py der timeline url erweitert, damit die timeline url erreichbar ist