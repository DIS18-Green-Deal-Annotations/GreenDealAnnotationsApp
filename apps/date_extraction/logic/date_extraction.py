import os, sys
import spacy #zusätzlich "python -m spacy download en_core_web_sm" ausführen
import csv
import pandas as pd
import numpy as np
import sqlite3

#custom scripts
import init_doc_obj
import doc_processing
import date_normalization

# import db
from date_extraction.models import DateExtraction

def add_data_to_db(df):
    df = df[pd.notnull(df['isodate'])] # delete all NaT (not null)
    df = df.sort_values(by=['isodate'], ascending = False) # sort df

    # schreibe die Daten aus dem df in die db

    model_instances = [DateExtraction(
        DocName = row['docname'],
        DocSentence = row['sentence'],
        DateLabel = row['datelabel'],
        IsoDate = row['isodate'],
    ) for row in df]

    DateExtraction.objects.bulk_create(model_instances)
    
    return print('data saved to db')


def main():

    # Load English tokenizer, tagger, parser and NER for spacys
    nlp = spacy.load("en_core_web_sm") 

    # creates list of objects for every document entry in init_doc_obj.py
    list_of_doc = init_doc_obj.main() 

    # creates df with all sentecnes from all documents
    df = doc_processing.main(list_of_doc, nlp) # doc.name | doc.sentence

    # extract date from sentence and normalize
    df = date_normalization.main(df, nlp) 

    # add data to db
    add_data_to_db(df)
    
if __name__=="__main__":
    main()