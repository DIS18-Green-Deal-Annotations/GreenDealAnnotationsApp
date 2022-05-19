import pandas as pd
import spacy
import numpy as np
import datetime as dt

def extract_date(df, nlp): # vera
    '''
    Adds new column to df with raw Date label from sentence. 
    ARGS: df = doc.name | doc.sentence
    RETURN: df = doc.name | doc.sentence | datelabel
    '''
    vera_df = pd.DataFrame()
    list = [] # empty list to store date entitys to append to df
    
    for index, row in df.iterrows():
        sentence = row['sentence']
        entitys = nlp(sentence)
        
        for entity in entitys.ents:
            if entity.label_ == "DATE":
                vera_df = vera_df.append(row)
                list.append(entity.text)

    vera_df['datelabel'] = list
    print('-> extract_date() ... done')
    return vera_df

def normalize_date(df): # helga
    ''' 
    function first converts strings with relative temporal expressions in given column to timestamp strings
    writes output in new column 'Date'
    function then converts all date strings in column 'Date' to short ISO format YYYY-MM-DD
    writes output in new column 'Isodate'
    invalid data converted to 'NaT' (not a time)
    ARGS: dataframe, column
    RETURN: df = # Docname | Sentence | DateLabel | Date | IsoDate
    '''
    # create a dictionary of relative temporal expressions
    # for working purposes, we will use datetime.now() for the prototype; needs to be replaced with document date later
    # keys will be collected successively from extracted relative temporal expressions later on
    relTempExp = {
        'this year':[str(dt.datetime.now().year)],
        'next year':[str(dt.datetime.now().year+1)],
        'last year':[str(dt.datetime.now().year-1)],
        'today':[str(dt.datetime.now())]
        }
    
    # set all strings to lower case to match with relTempExp dictionary
    df['datelabel'] = df['datelabel'].str.lower()

    # replace relative temporal expressions with date string values based on dictionary
    df = df.replace({'datelabel': relTempExp})

    # transform datelabel into isodate
    df['isodate'] = pd.to_datetime(df['datelabel'], errors='coerce').dt.date
    
    print('-> normalize_date() ... done')
    return df 

def main(df, nlp):
    '''
    Extract date from sentence and normalize
    ARGS: df = dataframe from doc_processing.py
    RETURN: df = # docname | sentence | datelabel | isodate
    '''
    vera_df = extract_date(df, nlp)
    helga_df = normalize_date(vera_df)

    return helga_df


